# News Search & Summarization API
# Build: docker build -t durmuhammad/news-api .
# Run: docker run -p 7000:7000 durmuhammad/news-api

FROM ubuntu:22.04

# Set environment
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/usr/local/bin:/usr/bin:${PATH}"

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    curl \
    wget \
    ca-certificates \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Install Chromium and chromedriver separately with proper deps
RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY summarization.py .

# Expose port 7000
EXPOSE 7000

# Run Flask application
CMD ["python3", "app.py"]
