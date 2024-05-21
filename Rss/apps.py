from django.apps import AppConfig


class RssConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Rss"

    def ready(self):
        from . import signals
