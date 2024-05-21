import os

from celery import Celery
from celery.schedules import crontab

from News.settings import CELERY_BROKER_URL
from Rss.config import CeleryQueueNameConfigEnum

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "News.settings")
FEED_UPDATE_INTERVAL_MINUTE = os.getenv("FEED_UPDATE_INTERVAL_MINUTE")
if FEED_UPDATE_INTERVAL_MINUTE is None:
    raise Exception("FEED_UPDATE_INTERVAL_MINUTE is not set")

app = Celery(
    "News",
    broker=CELERY_BROKER_URL,
)

app.conf.beat_schedule = {
    "rss-import": {
        "task": "Rss.tasks.rss.task_rss_import_from_feeds",
        "schedule": crontab(minute=f"*/{int(FEED_UPDATE_INTERVAL_MINUTE)}"),
        "options": {"queue": CeleryQueueNameConfigEnum.RSS_IMPORT.value},
    },
}
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
