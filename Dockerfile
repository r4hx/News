FROM python:3.12.2-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN useradd news_app -u 27424 -M --home "/app" -s /bin/false && \
    apt update && \
    apt install -y --no-install-recommends wget && \
    rm -rf /tmp/* /var/tmp/* /usr/share/doc/* /var/lib/apt/lists/*
    
USER news_app
COPY --chown=news_app:news_app . .
