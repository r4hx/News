import os

from bs4 import BeautifulSoup

from News.logger import make_logger
from Rss.exceptions.summary import (
    ExtractSummaryError,
    SummaryServiceResponseError,
    SummaryUrlNotFoundError,
)
from Rss.tools.http import HttpClient

logger = make_logger(name="tools-summary")

YANDEX_ENDPOINT = os.getenv("YANDEX_ENDPOINT")
if not YANDEX_ENDPOINT:
    raise Exception("YANDEX_ENDPOINT is not set")
YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
if not YANDEX_TOKEN:
    raise Exception("YANDEX_TOKEN is not set")


def send_url_to_yandex(url: str) -> str:
    """
    Отправить ссылку на статью в Яндекс 300.

    :param url: Ссылка на статью
    :return: Ссылка на статью в Яндекс 300
    :raises SummaryServiceResponseError: Если запрос к Яндекс 300 не удался
    :raises SummaryUrlNotFoundError: Если ссылка на статью в Яндекс 300 не удалось получить
    """
    logger.debug(f"Отправляем ссылку на статью в Яндекс 300: {url=}")
    client = HttpClient()
    response = client.post(
        url=YANDEX_ENDPOINT,
        json={"article_url": url},
        headers={"Authorization": f"OAuth {YANDEX_TOKEN}"},
    )

    if response.status_code != 200:
        logger.error(
            f"Не удалось отправить ссылку на статью в Яндекс 300: {url=} {response.status_code=}"
        )
        raise SummaryServiceResponseError

    sharing_url = response.json().get("sharing_url")
    if not sharing_url:
        logger.error(f"Не удалось получить ссылку на статью в Яндекс 300: {url=}")
        raise SummaryUrlNotFoundError

    return sharing_url


def get_summary_from_yandex(url: str) -> dict:
    """
    Получить пересказ статьи из Яндекс 300.

    :param url: Ссылка на статью в Яндекс 300
    :return: Пересказ статьи
    :raises SummaryServiceResponseError: Если запрос к Яндекс 300 не удался
    :raises ExtractSummaryError: Если пересказ статьи не удалось получить
    """
    logger.debug(f"Получаем пересказ статьи из Яндекс 300: {url=}")
    client = HttpClient()
    response = client.get(url=url)

    if response.status_code != 200:
        raise SummaryServiceResponseError

    description = extract_summary(response.text)

    return description


def extract_summary(html_content: str) -> str:
    """
    Извлечение описания статьи из HTML с использованием BeautifulSoup.

    :param html_content: HTML-код страницы
    :return: Описание статьи
    :raises ExtractSummaryError: Если описание статьи не удалось извлечь
    """
    soup = BeautifulSoup(html_content, "html.parser")
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and "content" in meta_tag.attrs:
        return str(" " + meta_tag.get("content"))
    else:
        raise ExtractSummaryError
