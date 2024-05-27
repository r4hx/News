import os

from celery import Task
from django.db import transaction

from News.celery import app
from News.logger import make_logger
from Rss.config import CeleryQueueNameConfigEnum
from Rss.models import Feed
from Rss.tools.rss import import_articles_from_feed
from Rss.tools.tasks import wait_for_object_to_save_in_store

logger = make_logger(name="task-rss")

CELERY_MAX_RETRIES = os.getenv("CELERY_MAX_RETRIES")
if not CELERY_MAX_RETRIES:
    raise EnvironmentError("CELERY_MAX_RETRIES is not set")

CELERY_COUNTDOWN = os.getenv("CELERY_COUNTDOWN")
if not CELERY_COUNTDOWN:
    raise EnvironmentError("CELERY_COUNTDOWN is not set")


@app.task(
    bind=True,
    queue=CeleryQueueNameConfigEnum.RSS_IMPORT.value,
    max_retries=int(CELERY_MAX_RETRIES),
)
def task_rss_import_from_feeds(self: Task, feed_id: int = 0):
    """
    Задача импорта статей из RSS.

    :param self: Ссылка на текущий объект задачи.
    :param feed_id: ID ленты RSS для импорта статей, если 0 - импорт из всех лент.
    """
    logger.debug("Импорт статей из RSS")
    try:
        with transaction.atomic():
            if feed_id == 0:
                logger.debug("Получение статей из всех лент")
                for feed in Feed.objects.all():
                    import_articles_from_feed(feed)
            else:
                logger.debug(f"Получение статей из ленты {feed_id=}")
                wait_for_object_to_save_in_store(model_class=Feed, pk=feed_id)
                feed = Feed.objects.get(pk=feed_id)
                import_articles_from_feed(feed=feed)
    except Feed.DoesNotExist as e:
        logger.error(f"Лента {feed_id=} не существует")
        raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))
    except Exception as e:
        logger.error("Не удалось получить статьи из RSS")
        raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))
