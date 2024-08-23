from django.core.management import BaseCommand

from Rss.models import Article
from Rss.tasks.related import task_set_related_articles_for_article


class Command(BaseCommand):
    """
    Очистить связанные записи у статей
    """

    def handle(self, *args, **options):
        articles = Article.objects.filter(related__isnull=True).order_by("-pk")
        for a in articles:
            task_set_related_articles_for_article.apply_async(
                kwargs={"article_id": a.pk}
            )
