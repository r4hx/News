from bs4 import BeautifulSoup

from News.logger import make_logger
from Rss.tools.http import HttpClient

logger = make_logger(name="tools-cover")


def get_image_from_source_url(url: str):
    """
    Получить изображение из источника
    """
    logger.debug(f"Получение изображения из {url=}")
    client = HttpClient()
    response = client.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        og_image_tag = soup.find("meta", property="og:image")
        if og_image_tag:
            image_url = og_image_tag.get("content")
            return image_url
        else:
            twitter_image_tag = soup.find("meta", property="twitter:image")
            if twitter_image_tag:
                image_url = twitter_image_tag.get("content")
                return image_url
            else:
                logger.debug(f"Не удалось получить изображение из {url=}")
                return None
    else:
        logger.exception(
            f"Ошибка получения изображения из {url=} с кодом {response.status_code}"
        )
        raise Exception(
            f"Ошибка получения изображения из {url=} с кодом {response.status_code}"
        )
