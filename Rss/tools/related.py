from datetime import timedelta

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Rss.config.article import ArticleStatusConfigEnum
from Rss.models import Article


def get_top_similar_titles(article_id: int, top_n=3):
    # Получаем основный заголовок
    main_article = Article.objects.get(pk=article_id)

    # Ограничиваем список заголовков на 1 неделю
    one_week_ago = main_article.created_at - timedelta(weeks=2)
    one_week_after = main_article.created_at + timedelta(weeks=2)

    titles_list = Article.objects.filter(
        status=ArticleStatusConfigEnum.PUBLISHED.value,
        created_at__range=(one_week_ago, one_week_after),
    )

    # Преобразуем queryset в список заголовков
    titles_list = [i.title for i in titles_list]

    # Создаем список заголовков, включая основной
    all_titles = [main_article.title] + titles_list

    # Инициализируем TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Преобразуем заголовки в TF-IDF матрицу
    tfidf_matrix = vectorizer.fit_transform(all_titles)

    # Рассчитываем косинусное сходство между первым заголовком и остальными
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

    # Находим индексы топ_n наиболее похожих заголовков
    top_indices = np.argsort(cosine_similarities)[-top_n:][::-1]

    # Составляем список топ_n заголовков и их сходства
    top_titles = [titles_list[i] for i in top_indices]

    articles_result = [
        Article.objects.get(title=i) for i in top_titles if i != main_article.title
    ]

    return articles_result


def set_article_related_articles(article_id: int):
    article = Article.objects.get(pk=article_id)
    article.related.add(*get_top_similar_titles(article_id=article_id))
