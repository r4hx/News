import os

from celery import Task
from django.db import transaction

from News.celery import app
from News.logger import make_logger
from Rss.config import ArticleStatusConfigEnum, CeleryQueueNameConfigEnum
from Rss.models import Article
from Rss.tools.summary import get_summary_from_yandex, send_url_to_yandex
from Rss.tools.tasks import wait_for_object_to_save_in_store

logger = make_logger(name="task-summary")

CELERY_MAX_RETRIES = os.getenv("CELERY_MAX_RETRIES")
if not CELERY_MAX_RETRIES:
    raise EnvironmentError("CELERY_MAX_RETRIES is not set")

CELERY_COUNTDOWN = os.getenv("CELERY_COUNTDOWN")
if not CELERY_COUNTDOWN:
    raise EnvironmentError("CELERY_COUNTDOWN is not set")


@app.task(
    bind=True,
    queue=CeleryQueueNameConfigEnum.SUMMARY.value,
    max_retries=int(CELERY_MAX_RETRIES),
)
def task_summary_text_from_article(self: Task, article_id: int):
    """
    Задача получения пересказа текста статьи.

    :param self: Ссылка на текущий объект задачи.
    :param article_id: ID статьи.
    """
    logger.debug(f"Создание пересказа для статьи {article_id=}")
    wait_for_object_to_save_in_store(model_class=Article, pk=article_id)
    try:
        with transaction.atomic():
            article = Article.objects.select_for_update().get(pk=article_id)
            sharing_url = send_url_to_yandex(url=article.url)
            summary = get_summary_from_yandex(url=sharing_url)
            article.summary_url = sharing_url
            article.summary = summary
            article.save()
    except Article.DoesNotExist as e:
        logger.error(f"Статья {article_id=} не существует")
        raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))
    except Exception as e:
        logger.error(f"Не удалось создать пересказ для статьи {article_id=}")
        with transaction.atomic():
            article = Article.objects.select_for_update().get(pk=article_id)
            article.retry_count = self.request.retries
            article.error_text = str(e)
            article.status = ArticleStatusConfigEnum.ERROR.value
            article.save()
            if self.request.retries != 0:
                logger.error(
                    f"Не удалось создать пересказ для статьи {article_id=}, повтор {self.request.retries}"
                )
        raise self.retry(exc=e, countdown=int(CELERY_COUNTDOWN))
