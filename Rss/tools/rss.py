from typing import List
from urllib.parse import urlparse

import feedparser

from News.logger import make_logger
from Rss.models import Feed
from Rss.tools.article import create_article

logger = make_logger(name="tools-rss")


def get_article_links_from_url(url: str) -> List[str]:
    """
    Получить ссылки на статьи из RSS-ленты.

    :param url: URL RSS-ленты.
    :return: Список ссылок на статьи.
    """
    logger.debug(f"Получение ссылок на статьи из {url=}")
    feed = feedparser.parse(url)
    article_links = [entry.link for entry in feed.entries if "link" in entry]
    logger.debug(f"Найдено {len(article_links)} ссылок на статьи")
    return article_links


def get_feed_name_from_url(url: str) -> str:
    """
    Получить название RSS-ленты.

    :param url: URL RSS-ленты.
    :return: Название RSS-ленты.
    """
    logger.debug(f"Получение названия RSS-ленты из {url=}")
    feed = feedparser.parse(url)
    if "title" in feed.feed:
        feed_title = feed.feed.title
        logger.debug(f"Название RSS-ленты: {feed_title}")
        return feed_title
    else:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        logger.debug(f"Название RSS-ленты не найдено, используется домен: {domain}")
        return domain


def get_feed_description_from_url(url: str) -> str:
    """
    Получить описание RSS-ленты.

    :param url: URL RSS-ленты.
    :return: Описание RSS-ленты.
    """
    logger.debug(f"Получение описания RSS-ленты из {url=}")
    feed = feedparser.parse(url)
    if "description" in feed.feed:
        feed_description = feed.feed.description
        logger.debug(f"Описание RSS-ленты: {feed_description}")
        return feed_description
    else:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        default_description = f"Статьи с сайта {domain}"
        logger.debug(
            f"Описание RSS-ленты не найдено, используется описание по умолчанию: {default_description}"
        )
        return default_description


def import_articles_from_feed(feed: Feed):
    """
    Импорт статей из конкретной ленты RSS.

    :param feed: Лента RSS.
    """
    try:
        logger.debug(f"Получение ссылок на статьи из RSS-ленты: {feed.url}")
        links = get_article_links_from_url(url=feed.url)
    except Exception as e:
        logger.error(f"Ошибка при получении ссылок из RSS-ленты {feed.url}: {e}")
        return

    created_articles_count = 0
    for link in links:
        if create_article(link, feed):
            created_articles_count += 1

    try:
        feed.save()
        logger.info(
            f"Импортировано {created_articles_count} статей из RSS-ленты {feed.url}"
        )
    except Exception as e:
        logger.error(f"Ошибка при сохранении состояния ленты {feed.url}: {e}")
