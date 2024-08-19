from django.contrib import admin

from Rss.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("pk", "source", "title", "status", "updated_at")
    list_display_links = ["pk"]
    search_fields = ["title", "summary"]
    list_filter = ["source", "status", "created_at"]
    date_hierarchy = "created_at"
    readonly_fields = [
        "pk",
        "source",
        "title",
        "summary",
        "summary_url",
        "image_url",
        "status",
        "get_article_url",
        "retry_count",
        "error_text",
        "created_at",
        "updated_at",
    ]
    ordering = ["-pk"]
    save_as = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:  # type: ignore
            qs = qs.filter(
                source__in=request.user.feeds.values_list("pk", flat=True),
            )
        return qs

    def get_article_url(self, obj):
        return obj.get_absolute_url()

    get_article_url.short_description = "Article URL"


admin.site.register(Article, ArticleAdmin)
