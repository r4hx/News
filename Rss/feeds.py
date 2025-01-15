from django.contrib.syndication.views import Feed
from django.utils.html import linebreaks
from django.utils.safestring import mark_safe

from Rss.config import ArticleStatusConfigEnum
from Rss.models import Article
from Rss.models import Feed as FeedModel


class FeedArticlesFeed(Feed):
    def get_object(self, request, *args, **kwargs):
        return FeedModel.objects.get(slug=kwargs["slug"])

    def title(self, obj):
        return f"{obj.name}"

    def link(self, obj):
        return obj.url

    def items(self, obj):
        return Article.objects.filter(
            source=obj,
            status=ArticleStatusConfigEnum.PUBLISHED.value,
        ).order_by("-created_at")[:100]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if item.image_url:
            image_html = f'<img src="{item.image_url}" alt="{item.title}" style="max-width:100%;" /><br><br>'
        else:
            image_html = ""
        return mark_safe(f"{image_html}{linebreaks(item.summary)}{item.get_full_url()}")

    def item_pubdate(self, item):
        return item.created_at
