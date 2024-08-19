from django.shortcuts import get_object_or_404, render

from Rss.models import Article, Feed
from Web.tools.idhide import decode_id


def article_detail_view(request, slug, encoded_id):
    source = get_object_or_404(Feed, slug=slug)
    article_id = decode_id(encoded_id)
    article = get_object_or_404(Article, source=source, id=article_id)
    return render(
        request,
        "article.html",
        {"article": article},
    )
