FROM python:3.13.5-slim

# Install system dependencies including Chrome and additional libs
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg2 \
    chromium \
    chromium-driver \
    xvfb \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libx11-xcb1 \
    libxtst6 \
    libxss1 \
    libasound2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable for Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMIUM_PATH=/usr/bin/chromium

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
