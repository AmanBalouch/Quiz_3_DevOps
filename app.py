from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from summarization import summarize_text
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REGISTRATION_DATA = {
    "registration": "FA23-BAI-012",
    "newssource": "AbbtakTv"
}

def get_chrome_options():
    """Chrome options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-web-resources")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    return chrome_options

def search_news(keyword):
    """Search for news"""
    try:
        driver = webdriver.Chrome(options=get_chrome_options())
        search_url = f"https://abbtakk.tv/?s={keyword}"
        logger.info(f"Searching: {search_url}")
        
        driver.get(search_url)
        time.sleep(3)
        
        links = driver.find_elements(By.TAG_NAME, "a")
        
        for link in links:
            href = link.get_attribute("href")
            text = link.text.strip()
            
            if not href or not text or len(text) < 5:
                continue
            if any(x in href.lower() for x in ["facebook", "twitter", "#", "javascript"]):
                continue
            if href.startswith("http"):
                logger.info(f"Found: {text}")
                driver.quit()
                return href, text
        
        driver.quit()
        return None, None
        
    except Exception as e:
        logger.error(f"Error: {e}")
        try:
            driver.quit()
        except:
            pass
        return None, None

def fetch_article_content(url):
    """Fetch article content"""
    try:
        driver = webdriver.Chrome(options=get_chrome_options())
        driver.get(url)
        time.sleep(2)
        
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        content = " ".join([p.text for p in paragraphs if p.text])
        
        driver.quit()
        return content if content else "No content"
        
    except Exception as e:
        logger.error(f"Error fetching: {e}")
        try:
            driver.quit()
        except:
            pass
        return "Error"

@app.route('/get', methods=['GET'])
def get_news():
    """API endpoint"""
    try:
        keyword = request.args.get('keyword', '') or request.args.get('q', '')
        keyword = keyword.strip().strip('"\'')
        
        if not keyword:
            return jsonify({"error": "Missing keyword parameter"}), 400
        
        logger.info(f"Request: {keyword}")
        
        url, title = search_news(keyword)
        if not url:
            return jsonify({"error": f"No articles found for: {keyword}"}), 404
        
        content = fetch_article_content(url)
        summary = summarize_text(content)
        
        response = {
            "registration": REGISTRATION_DATA["registration"],
            "newssource": REGISTRATION_DATA["newssource"],
            "keyword": keyword,
            "url": url,
            "summary": summary
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
