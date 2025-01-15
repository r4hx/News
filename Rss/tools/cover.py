from bs4 import BeautifulSoup

from News.logger import make_logger
from Rss.exceptions.cover import CoverStatusCodeError
from Rss.tools.http import HttpClient

logger = make_logger(name="tools-cover")


def get_image_from_source_url(url: str) -> str:
    """
    Получить URL изображения из источника по заданному URL.

    :param url: URL источника
    :return: URL изображения или None, если изображение не найдено
    """
    logger.debug(f"Получение изображения из {url=}")
    client = HttpClient()
    response = client.get(url)

    if response.status_code != 200:
        logger.error(
            f"Ошибка получения изображения из {url=} с кодом {response.status_code=}"
        )
        raise CoverStatusCodeError

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    image_url = extract_image_url(soup)
    if image_url:
        logger.info(f"Найдено изображение: {image_url}")
    else:
        logger.info(f"Не удалось найти изображение в {url=}")

    return image_url


def extract_image_url(soup: BeautifulSoup) -> str:
    """
    Извлечь URL изображения из HTML-контента.

    :param soup: Объект BeautifulSoup с HTML-контентом
    :return: URL изображения или None, если изображение не найдено
    """
    og_image_tag = soup.find("meta", attrs={"property": "og:image"}) or soup.find(
        "meta", attrs={"name": "og:image"}
    )
    if og_image_tag and og_image_tag.get("content"):
        return og_image_tag["content"]

    twitter_image_tag = soup.find(
        "meta", attrs={"property": "twitter:image"}
    ) or soup.find("meta", attrs={"name": "twitter:image"})
    if twitter_image_tag and twitter_image_tag.get("content"):
        return twitter_image_tag["content"]

    default_image = "https://egorovegor.ru/wp-content/uploads/stati.jpeg"
    return default_image
