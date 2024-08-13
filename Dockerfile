# Use the official Python image as a base
FROM python:3.9-slim

# Install dependencies
RUN for i in 1 2 3 4 5; do \
        apt-get update -y && \
        apt-get install -y --no-install-recommends \
            wget \
            unzip \
            libgconf-2-4 \
            libnss3 \
            libfontconfig1 \
            libx11-6 \
            libx11-xcb1 \
            libxcb1 \
            libxcomposite1 \
            libxcursor1 \
            libxdamage1 \
            libxext6 \
            libxfixes3 \
            libxi6 \
            libxrandr2 \
            libxrender1 \
            libxss1 \
            libxtst6 \
            fonts-liberation \
            libasound2 \
            libatk-bridge2.0-0 \
            libatspi2.0-0  \
            libgtk-3-0 && \
        break || sleep 15; \
    done && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN apt-get update && apt-get install xvfb -y


RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable


# Install Chrome
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.99/linux64/chrome-linux64.zip \
    && unzip chrome-linux64.zip -d /opt/ \
    && ln -s /opt/chrome-linux64/chrome /usr/bin/chrome \
    && rm chrome-linux64.zip

# Install ChromeDriver
# RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.99/linux64/chromedriver-linux64.zip \
#     && unzip chromedriver-linux64.zip \
#     && mv chromedriver-linux64/chromedriver /usr/local/bin/ \
#     && rm -rf chromedriver-linux64.zip chromedriver-linux64 \
#     && chmod +x /usr/local/bin/chromedriver \
#     && /usr/local/bin/chromedriver --version


RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]



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
