from bs4 import BeautifulSoup

from News.logger import make_logger
from Rss.tools.http import HttpClient

logger = make_logger(name="tools-titler")


def get_title_from_source_url(url: str) -> str:
    """
    Получить название статьи из источника по URL.
    """
    logger.debug(f"Получение названия статьи из {url=}")
    client = HttpClient()
    response = client.get(url)

    if response.status_code != 200:
        logger.error(
            f"Ошибка получения названия статьи из {url=} с кодом {response.status_code}"
        )
        raise Exception(
            f"Ошибка получения названия статьи из {url=} с кодом {response.status_code}"
        )

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    title = _extract_title(soup)
    if title:
        return title
    else:
        logger.error(f"Не удалось получить название статьи из {url=}")
        raise Exception(f"Не удалось получить название статьи из {url=}")


def _extract_title(soup: BeautifulSoup) -> str:
    """
    Извлечение названия статьи из HTML с использованием BeautifulSoup.

    :param soup: Объект BeautifulSoup
    :return: Название статьи или None, если не найдено
    """
    try:
        meta_tag = soup.find("meta", property="og:title")
        if meta_tag and "content" in meta_tag.attrs:
            return meta_tag["content"]
    except Exception as e:
        logger.warning("Ошибка при попытке найти meta тег: ", exc_info=e)

    try:
        title_tag = soup.find("title")
        if title_tag:
            return title_tag.text
    except Exception as e:
        logger.warning("Ошибка при попытке найти title тег: ", exc_info=e)

    return None
