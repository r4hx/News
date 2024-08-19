from django.urls import path

from Web.views import article_detail_view

urlpatterns = [
    path(
        "<slug>/<slug:encoded_id>/",
        article_detail_view,
        name="article_detail",
    ),
]
