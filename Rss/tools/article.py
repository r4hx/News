from django.db import IntegrityError, transaction

from News.logger import make_logger
from Rss.models import Article, Feed
from Rss.tools.cover import get_image_from_source_url

logger = make_logger(name="tools-article")


def create_article(link: str, feed: Feed) -> bool:
    """
    Создает или получает статью по ссылке и источнику.

    :param link: Ссылка на статью.
    :param feed: Источник (RSS-лента).
    :return: True, если статья была создана, False если уже существовала или произошла ошибка.
    """
    try:
        _, created = Article.objects.get_or_create(url=link, source=feed)
        if created:
            logger.debug(f"Создана новая статья: {link}")
        return created
    except IntegrityError as e:
        logger.error(f"Ошибка целостности данных при создании статьи {link}: {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при создании статьи {link}: {e}")
    return False


def update_article_cover(article_id: int):
    """
    Обновление обложки статьи.

    :param article_id: ID статьи.
    """
    with transaction.atomic():
        article = Article.objects.select_for_update().get(pk=article_id)
        logger.debug(f"Получение обложки для статьи: {article_id}")
        cover = get_image_from_source_url(url=article.url)
        article.image_url = cover
        article.save()
        logger.info(f"Обложка для статьи с ID {article_id} успешно обновлена")
