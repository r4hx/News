import os

from django.db import transaction

from News.celery import app
from News.logger import make_logger
from Rss.config import ArticleStatusConfigEnum, CeleryQueueNameConfigEnum
from Rss.models import Article
from Rss.tools.summary import get_summary_from_yandex, send_url_to_yandex

logger = make_logger(name="task-summary")

CELERY_MAX_RETRIES = os.getenv("CELERY_MAX_RETRIES")
if CELERY_MAX_RETRIES is None:
    raise Exception("CELERY_MAX_RETRIES is not set")

CELERY_COUNTDOWN = os.getenv("CELERY_COUNTDOWN")
if CELERY_COUNTDOWN is None:
    raise Exception("CELERY_COUNTDOWN is not set")


@app.task(
    bind=True,
    queue=CeleryQueueNameConfigEnum.SUMMARY.value,
    max_retries=int(CELERY_MAX_RETRIES),
)
def task_summary_text_from_article(self, article_id: int):
    """
    Задача получения пересказа текста статьи
    """
    logger.debug(f"Создание пересказа для статьи {article_id=}")
    try:
        with transaction.atomic():
            article = Article.objects.select_for_update().get(pk=article_id)
            sharing_url = send_url_to_yandex(url=article.url)
            summary = get_summary_from_yandex(url=sharing_url)
            article.summary_url = sharing_url
            article.summary = summary
            article.save()
    except Exception as e:
        logger.exception(f"Не удалось создать пересказ для статьи {article_id=}")
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
