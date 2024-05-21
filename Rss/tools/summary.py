import os

from bs4 import BeautifulSoup

from News.logger import make_logger
from Rss.tools.http import HttpClient

logger = make_logger(name="tools-summary")

YANDEX_ENDPOINT = os.getenv("YANDEX_ENDPOINT")
if YANDEX_ENDPOINT is None:
    raise Exception("YANDEX_ENDPOINT is not set")
YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
if YANDEX_TOKEN is None:
    raise Exception("YANDEX_TOKEN is not set")


def send_url_to_yandex(url: str) -> str:
    """
    Отправить ссылку на статью в Яндекс 300
    """
    logger.debug(f"Отправка ссылки на статью в Яндекс 300: {url=}")
    client = HttpClient()
    response = client.post(
        YANDEX_ENDPOINT,
        json={"article_url": url},
        headers={"Authorization": f"OAuth {YANDEX_TOKEN}"},
    )
    if response.status_code == 200:
        sharing_url = response.json().get("sharing_url")
        return sharing_url
    else:
        logger.exception(
            f"Ошибка отправки ссылки на статью в Яндекс 300: {url=} с кодом {response.status_code}"
        )
        raise Exception(
            f"Ошибка отправки ссылки на статью в Яндекс 300: {url=} с кодом {response.status_code}"
        )


def get_summary_from_yandex(url: str) -> dict:
    """
    Получить пересказ статьи из Яндекс 300
    """
    logger.debug(f"Получение пересказа статьи из Яндекс 300: {url=}")
    client = HttpClient()
    response = client.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        meta_tag = soup.find("meta", attrs={"name": "description"})
        description = (
            meta_tag.get("content")
            if meta_tag.get("content") is None
            else str(" " + meta_tag.get("content"))
        )
        return description
    else:
        logger.exception(
            f"Ошибка получения пересказа статьи из Яндекс 300: {url=} с кодом {response.status_code}"
        )
        raise Exception(
            f"Ошибка получения пересказа статьи из Яндекс 300: {url=} с кодом {response.status_code}"
        )
