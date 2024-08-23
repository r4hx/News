from django.core.management import BaseCommand

from Rss.models import Article


class Command(BaseCommand):
    """
    Очистить связанные записи у статей
    """

    def handle(self, *args, **options):
        articles = Article.objects.filter(related__isnull=False)
        for a in articles:
            a.related.clear()
