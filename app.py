from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from summarization import summarize_text
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your registration details
REGISTRATION_DATA = {
    "registration": "FA23-BAI-012",
    "newssource": "AbbtakTv"
}

def get_chrome_options():
    """Configure Chrome options for headless browsing"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    return chrome_options

def search_news(keyword):
    """Search for news article on abbtakk.tv and return the first result"""
    try:
        driver = None
        driver = webdriver.Chrome(options=get_chrome_options())
        
        # Construct search URL
        search_url = f"https://abbtakk.tv/?s={keyword}"
        logger.info(f"Searching for: {search_url}")
        
        driver.get(search_url)
        time.sleep(3)  # Wait for page to load
        
        # Try to find the first article link
        wait = WebDriverWait(driver, 10)
        
        try:
            # Try multiple methods to find articles
            wait = WebDriverWait(driver, 10)
            article = None
            
            # Method 1: Try XPath to find any link with article in href or that looks like article
            try:
                article = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/')][@href!='#']"))
                )
            except:
                pass
            
            # Method 2: Try common CSS selectors
            if not article:
                selectors = ["article a", ".post a", ".entry-title a", "h2 a", "h3 a", ".title a"]
                for selector in selectors:
                    try:
                        article = driver.find_element(By.CSS_SELECTOR, selector)
                        if article and article.get_attribute("href"):
                            break
                    except:
                        continue
            
            # Method 3: Get first non-empty link
            if not article:
                all_links = driver.find_elements(By.TAG_NAME, "a")
                for link in all_links:
                    href = link.get_attribute("href")
                    if href and ("article" in href.lower() or ".com/" in href):
                        article = link
                        break
            
            if not article:
                logger.error("No article link found")
                return None, None
                
            article_url = article.get_attribute("href")
            article_title = article.text.strip() or "Article"
            
            logger.info(f"Found article: {article_title}")
            logger.info(f"Article URL: {article_url}")
            
            return article_url, article_title
            
        except Exception as e:
            logger.error(f"Error finding article: {e}")
            return None, None
            
    except Exception as e:
        logger.error(f"Error in search_news: {e}")
        return None, None
    finally:
        if driver:
            driver.quit()

def fetch_article_content(article_url):
    """Fetch the content of the article"""
    try:
        driver = None
        driver = webdriver.Chrome(options=get_chrome_options())
        driver.get(article_url)
        time.sleep(2)
        
        # Extract article content
        try:
            # Try common article content selectors
            selectors = [
                "article .entry-content",
                "article p",
                ".post-content p",
                ".content p",
                "main p"
            ]
            
            content_parts = []
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for elem in elements[:10]:  # Get first 10 paragraphs
                            text = elem.text.strip()
                            if text:
                                content_parts.append(text)
                        if content_parts:
                            break
                except:
                    continue
            
            article_content = " ".join(content_parts)
            return article_content if article_content else "No content extracted"
            
        except Exception as e:
            logger.error(f"Error extracting content: {e}")
            return "Error extracting content"
            
    except Exception as e:
        logger.error(f"Error fetching article: {e}")
        return "Error fetching article"
    finally:
        if driver:
            driver.quit()

@app.route('/get', methods=['GET'])
def get_news():
    """
    API endpoint to search for news and return summary
    Query parameter: keyword (string)
    Returns: JSON with registration, newssource, keyword, url, summary
    """
    try:
        keyword = request.args.get('keyword', '').strip()
        
        if not keyword:
            return jsonify({
                "error": "Missing 'keyword' query parameter"
            }), 400
        
        logger.info(f"Processing request for keyword: {keyword}")
        
        # Search for the article
        article_url, article_title = search_news(keyword)
        
        if not article_url:
            return jsonify({
                "error": f"No articles found for keyword: {keyword}"
            }), 404
        
        # Fetch article content
        article_content = fetch_article_content(article_url)
        
        # Summarize the content
        summary = summarize_text(article_content)
        
        # Prepare response
        response = {
            "registration": REGISTRATION_DATA["registration"],
            "newssource": REGISTRATION_DATA["newssource"],
            "keyword": keyword,
            "url": article_url,
            "summary": summary
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in /get endpoint: {e}")
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
