import os

from celery import Task
from django.db import transaction

from News.celery import app
from News.logger import make_logger
from Rss.config import CeleryQueueNameConfigEnum
from Rss.models import Article
from Rss.tools.cover import get_image_from_source_url

logger = make_logger(name="task-cover")

CELERY_MAX_RETRIES = os.getenv("CELERY_MAX_RETRIES")
if not CELERY_MAX_RETRIES:
    raise EnvironmentError("CELERY_MAX_RETRIES is not set")

CELERY_COUNTDOWN = os.getenv("CELERY_COUNTDOWN")
if not CELERY_COUNTDOWN:
    raise EnvironmentError("CELERY_COUNTDOWN is not set")


@app.task(
    bind=True,
    queue=CeleryQueueNameConfigEnum.COVER.value,
    max_retries=int(CELERY_MAX_RETRIES),
)
def task_set_cover_from_article(self: Task, article_id: int):
    """
    Задача указания обложки статьи.

    :param self: Ссылка на текущий объект задачи.
    :param article_id: ID статьи.
    """
    logger.debug(f"Создание обложки для статьи {article_id=}")
    try:
        with transaction.atomic():
            article = Article.objects.select_for_update().get(pk=article_id)
            cover = get_image_from_source_url(url=article.url)
            article.image_url = cover
            article.save()
    except Article.DoesNotExist as e:
        logger.error(f"Статья {article_id=} не существует")
        raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))
    except Exception as e:
        logger.error(f"Не удалось создать обложку для статьи {article_id=}")
        raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))
