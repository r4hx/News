import os

from celery import Task

from News.celery import app
from News.logger import make_logger
from Rss.config import CeleryQueueNameConfigEnum
from Rss.models import Article
from Rss.tools.related import set_article_related_articles
from Rss.tools.tasks import wait_for_object_to_save_in_store

logger = make_logger(name="task-related")

CELERY_MAX_RETRIES = os.getenv("CELERY_MAX_RETRIES")
if not CELERY_MAX_RETRIES:
    raise EnvironmentError("CELERY_MAX_RETRIES is not set")

CELERY_COUNTDOWN = os.getenv("CELERY_COUNTDOWN")
if not CELERY_COUNTDOWN:
    raise EnvironmentError("CELERY_COUNTDOWN is not set")


@app.task(
    bind=True,
    queue=CeleryQueueNameConfigEnum.RELATED.value,
    max_retries=int(CELERY_MAX_RETRIES),
)
def task_set_related_articles_for_article(self: Task, article_id: int):
    """
    Задача указания связанных статей.

    :param self: Ссылка на текущий объект задачи.
    :param article_id: ID статьи.
    """
    logger.debug(f"Ищем похожие записи для статьи {article_id=}")
    try:
        wait_for_object_to_save_in_store(model_class=Article, pk=article_id)
        set_article_related_articles(article_id=article_id)
    except Article.DoesNotExist as e:
        logger.error(f"Статья {article_id=} не существует")
        raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))
    except Exception as e:
        logger.error(f"Не удалось получить похожие записи для статьи {article_id=}")
        raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))
