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




# Install Firefox ESR 102.0
RUN wget -O firefox.tar.bz2 "https://ftp.mozilla.org/pub/firefox/releases/102.0esr/linux-x86_64/en-US/firefox-102.0esr.tar.bz2" \
    && tar xjf firefox.tar.bz2 -C /opt/ \
    && ln -s /opt/firefox/firefox /usr/bin/firefox

# Install geckodriver 0.31.0 (compatible with Firefox 102)
RUN wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz \
    && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
    && chmod +x /opt/geckodriver \
    && ln -s /opt/geckodriver /usr/local/bin/geckodriver






# Set display port to avoid crash
ENV DISPLAY=:99

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


RUN echo '#!/bin/bash\npython bot.py' > entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
