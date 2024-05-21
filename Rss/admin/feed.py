from typing import Any

from django.contrib import admin

from Rss.models import Feed


class FeedAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "url", "feed_url", "updated_at")
    list_display_links = ["pk"]
    date_hierarchy = "created_at"
    readonly_fields = [
        "pk",
        "slug",
        "description",
        "feed_url",
        "created_at",
        "updated_at",
    ]
    ordering = ["-pk"]
    save_as = True

    def feed_url(self, obj):
        return obj.feed_url

    feed_url.short_description = "Cсылка на RSS канал"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:  # type: ignore
            qs = qs.filter(
                pk__in=request.user.feeds.values_list("pk", flat=True),
            )
        return qs

    def save_model(self, request, obj, form, change):
        if request.user.feeds.filter(pk=obj.pk).exists():
            obj.save()
        else:
            obj.save()
            request.user.feeds.add(obj)


admin.site.register(Feed, FeedAdmin)
