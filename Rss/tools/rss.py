from urllib.parse import urlparse

import feedparser

from News.logger import make_logger

logger = make_logger(name="tools-rss")


def get_article_links_from_url(url: str) -> list:
    """
    Получить ссылки на статьи из RSS-ленты
    """
    logger.debug(f"Получение ссылок на статьи из {url=}")
    feed = feedparser.parse(url)
    article_links = []
    for entry in feed.entries:
        if "link" in entry:
            article_links.append(entry.link)
    return article_links


def get_feed_name_from_url(url: str) -> str:
    """
    Получить название RSS-ленты
    """
    logger.debug(f"Получение названия RSS-ленты из {url=}")
    feed = feedparser.parse(url)
    if "title" in feed.feed:
        return feed.feed.title
    else:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return domain


def get_feed_description_from_url(url: str) -> str:
    """
    Получить описание RSS-ленты
    """
    logger.debug(f"Получение описания RSS-ленты из {url=}")
    feed = feedparser.parse(url)
    if "description" in feed.feed:
        return feed.feed.description
    else:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return f"Статьи с сайта {domain}"
