# News Search & Summarization API

A Flask-based REST API that searches for news articles from AbbtakTv.com, fetches their content, and provides AI-powered summaries.

**Registration:** FA23-BAI-012  
**Course:** CSC413 - DevOps for Cloud Computing  
**News Source:** https://abbtakk.tv/

## Features

- **Selenium Automation**: Automated web scraping with Chrome headless browser
- **News Search**: Search for articles by keyword on abbtakk.tv
- **Content Extraction**: Automatically extracts article content
- **AI Summarization**: Uses transformer-based models for intelligent summarization with fallback to extractive method
- **REST API**: Simple GET endpoint on port 7000
- **Docker Support**: Ready for containerization

## Project Structure

```
.
├── app.py                 # Main Flask application
├── summarization.py       # Summarization module
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Docker Compose orchestration
└── README.md             # This file
```

## Installation

### Option 1: Local Setup

1. **Install Python 3.11+** and Chrome browser

2. **Download ChromeDriver** from https://chromedriver.chromium.org/ (must match your Chrome version)

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:7000`

### Option 2: Docker Setup (Recommended)

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually:**
   ```bash
   docker build -t news-api .
   docker run -p 7000:7000 news-api
   ```

## API Usage

### Endpoint: `/get`

**Method:** GET

**Query Parameters:**
- `keyword` (required, string): Search keyword for news articles

**Example Request:**
```
http://localhost:7000/get?keyword=pakistan
```

**Response:**
```json
{
    "registration": "FA23-BAI-012",
    "newssource": "AbbtakTv",
    "keyword": "pakistan",
    "url": "https://abbtakk.tv/article/...",
    "summary": "Pakistan's economy shows signs of improvement... Key initiatives include..."
}
```

### Health Check: `/health`

**Method:** GET

**Example:**
```
http://localhost:7000/health
```

**Response:**
```json
{
    "status": "OK"
}
```

## How It Works

1. **Search Request**: User sends a GET request with a keyword
2. **Web Scraping**: Selenium opens Chrome browser and searches abbtakk.tv
3. **Article Extraction**: Finds the first search result article link
4. **Content Fetching**: Navigates to the article and extracts content
5. **Summarization**: Uses transformer models (BART) to summarize, with fallback to extractive method
6. **Response**: Returns JSON with registration, news source, keyword, URL, and summary

## Technical Details

### Selenium Configuration
- **Headless Mode**: Runs without opening visible browser window
- **No Sandbox**: Required for Docker environments
- **Custom User-Agent**: Mimics real browser requests

### Summarization
- **Primary Method**: Facebook's BART transformer model
- **Fallback Method**: Extractive summarization based on sentence scoring
- **Output**: 3-sentence summary (configurable)

## Error Handling

- Returns 400 if keyword parameter is missing
- Returns 404 if no articles are found for the keyword
- Returns 500 for server errors with error details

## Dependencies

- **Flask**: Web framework
- **Selenium**: Web automation and scraping
- **Transformers**: AI-powered text summarization
- **Torch**: Deep learning framework for transformers

## Testing

Test the API using curl:

```bash
# Test with a keyword
curl "http://localhost:7000/get?keyword=election"

# Test health check
curl "http://localhost:7000/health"

# Test missing keyword
curl "http://localhost:7000/get"
```

## Notes

- The API automatically starts the service when the Docker container runs
- Chrome browser is included in the Docker image
- Summarization models are downloaded on first use (requires internet)
- Response time depends on article length and summarization model loading

## Troubleshooting

**"Chrome not found"**: Install Chromium or Chrome browser

**"No articles found"**: Website structure might have changed; verify the CSS selectors

**"Timeout errors"**: Increase wait times in the code if the website is slow

**Memory issues**: Docker image is ~2GB; ensure sufficient system resources

## License

COMSATS University Islamabad, Department of Computer Science
