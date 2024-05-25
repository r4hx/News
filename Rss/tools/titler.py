from bs4 import BeautifulSoup

from News.logger import make_logger
from Rss.tools.http import HttpClient

logger = make_logger(name="tools-titler")


def get_title_from_source_url(url: str) -> str:
    """
    Получить название статьи из источника
    """
    logger.debug(f"Получение названия статьи из {url=}")
    client = HttpClient()
    response = client.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        meta_tag = soup.find("meta", property="og:title")
        try:
            if meta_tag and "content" in meta_tag.attrs:
                title = meta_tag["content"]
            else:
                raise AttributeError(
                    "Не найден тег <meta property='og:title' content='...'>"
                )
        except AttributeError:
            logger.exception(
                f"Не удалось получить название статьи из {url=} с кодом {response.status_code}"
            )
            raise Exception(
                f"Не удалось получить название статьи из {url=} с кодом {response.status_code}"
            )
        return title
    else:
        logger.exception(
            f"Ошибка получения названия статьи из {url=} с кодом {response.status_code}"
        )
        raise Exception(
            f"Ошибка получения названия статьи из {url=} с кодом {response.status_code}"
        )
