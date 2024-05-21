## RSS feed samarizer

## Description

This project is a service for summarizing RSS feeds. If you use RSS for news, you can add your sources to the project and get a new RSS feed with summarized articles.

Even if the source feeds provide a brief summary of the articles, the service will analyze the pages and extract the main ideas from them.

## Setup

You will need Docker and docker-compose to start the project. Follow these steps:

Clone the repository:

```
git clone <url_repository>
```

Run the container build:
 
```
make build
```

## Configuration

Copy the `.env.example` file to `.env` and fill in the mandatory parameters:

- YANDEX_TOKEN = token from the https://300.ya.ru service (at the bottom of the page, click API and the “get token” button will appear)

## Usage

To start the project use the command:

```
make 
```

and open the link in a browser `http://127.0.0.1`.

To stop the project and clear the cache, use:

```
make stop
```
