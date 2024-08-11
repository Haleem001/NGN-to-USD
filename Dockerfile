# Use the official Python image as a base
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    default-jdk \
    gnupg \
    curl \
    && rm -rf /var/lib/apt/lists/*
# Install latest stable Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/* \
    && google-chrome --version
 


# Install Chrome
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.99/linux64/chrome-linux64.zip \
    && unzip chrome-linux64.zip -d /opt/ \
    && ln -s /opt/chrome-linux64/chrome /usr/bin/chrome \
    && rm chrome-linux64.zip

# Install ChromeDriver
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.99/linux64/chromedriver-linux64.zip \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip

# Set Chrome and ChromeDriver in PATH
ENV PATH="/opt/chrome-linux64:/usr/local/bin:${PATH}"




# Set display port to avoid crash
ENV DISPLAY=:99

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "bot.py"]
