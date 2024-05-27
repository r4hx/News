import os

from celery import Task

from News.celery import app
from News.logger import make_logger
from Rss.config import CeleryQueueNameConfigEnum
from Rss.models import Article
from Rss.tools.article import update_article_cover
from Rss.tools.tasks import wait_for_object_to_save_in_store

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
        wait_for_object_to_save_in_store(model_class=Article, pk=article_id)
        update_article_cover(article_id=article_id)
    except Article.DoesNotExist as e:
        logger.error(f"Статья {article_id=} не существует")
        raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))
    except Exception as e:
        logger.error(f"Не удалось создать обложку для статьи {article_id=}")
        raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))
