from django.urls import path

from Rss.feeds import FeedArticlesFeed

urlpatterns = [
    path("<slug>/", FeedArticlesFeed(), name="feed-articles"),
]
