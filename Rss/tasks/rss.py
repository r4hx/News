import os

from News.celery import app
from News.logger import make_logger
from Rss.config import CeleryQueueNameConfigEnum
from Rss.models import Article, Feed
from Rss.tools.rss import get_article_links_from_url

logger = make_logger(name="task-rss")

CELERY_MAX_RETRIES = os.getenv("CELERY_MAX_RETRIES")
if CELERY_MAX_RETRIES is None:
    raise Exception("CELERY_MAX_RETRIES is not set")

CELERY_COUNTDOWN = os.getenv("CELERY_COUNTDOWN")
if CELERY_COUNTDOWN is None:
    raise Exception("CELERY_COUNTDOWN is not set")


@app.task(
    bind=True,
    queue=CeleryQueueNameConfigEnum.RSS_IMPORT.value,
    max_retries=int(CELERY_MAX_RETRIES),
)
def task_rss_import_from_feeds(self, feed_id: int = 0):
    """
    Задача импорта статей из RSS
    """
    try:
        if feed_id == 0:
            logger.debug("Получение статей из всех лент")
            feeds = Feed.objects.all()
            for f in feeds:
                links = get_article_links_from_url(url=f.url)
                for link in links:
                    Article.objects.get_or_create(
                        url=link,
                        source=f,
                    )
                f.save()
        else:
            logger.debug(f"Получение статей из ленты {feed_id=}")
            try:
                feed = Feed.objects.get(pk=feed_id)
            except Feed.DoesNotExist:
                logger.exception(f"Лента {feed_id=} не существует")
                raise self.retry(
                    exc=Exception(f"Лента {feed_id=} не существует"),
                    countdown=int(CELERY_COUNTDOWN),
                )

            links = get_article_links_from_url(url=feed.url)
            for link in links:
                Article.objects.get_or_create(
                    url=link,
                    source=feed,
                )
            feed.save()
    except Exception as e:
        logger.exception("Не удалось получить статьи из RSS")
        raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))
