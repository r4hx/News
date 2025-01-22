import os
import random
import time

import httpx

from News.logger import make_logger

logger = make_logger(name="tools-http")

HTTP_RESPONSE_TIMEOUT = os.getenv("HTTP_RESPONSE_TIMEOUT")
HTTP_TIME_SLEEP_AFTER_TOO_MANY_CONNECTION = os.getenv(
    "HTTP_TIME_SLEEP_AFTER_TOO_MANY_CONNECTION"
)
HTTP_TIME_SLEEP_BETWEEN_CONNECTION = os.getenv("HTTP_TIME_SLEEP_BETWEEN_CONNECTION")

if not HTTP_RESPONSE_TIMEOUT:
    raise EnvironmentError("HTTP_RESPONSE_TIMEOUT is not set")
if not HTTP_TIME_SLEEP_AFTER_TOO_MANY_CONNECTION:
    raise EnvironmentError("HTTP_TIME_SLEEP_AFTER_TOO_MANY_CONNECTION is not set")
if not HTTP_TIME_SLEEP_BETWEEN_CONNECTION:
    raise EnvironmentError("HTTP_TIME_SLEEP_BETWEEN_CONNECTION is not set")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
]


class HttpClient:
    """
    Класс для работы с HTTP запросами
    """

    def __init__(
        self,
        timeout: int = int(HTTP_RESPONSE_TIMEOUT),
        time_sleep_after_too_many_connection: int = int(
            HTTP_TIME_SLEEP_AFTER_TOO_MANY_CONNECTION
        ),
        time_sleep_between_connection: int = int(HTTP_TIME_SLEEP_BETWEEN_CONNECTION),
        **kwargs,
    ):
        self.timeout = timeout
        self.time_sleep_after_too_many_connection = time_sleep_after_too_many_connection
        self.time_sleep_between_connection = time_sleep_between_connection
        self.client = httpx.Client(timeout=timeout, follow_redirects=True, **kwargs)

    def _handle_rate_limit(self, response: httpx.Response):
        """
        Обработка лимита запросов (429 Too Many Requests)
        """
        if response.status_code == 429:
            logger.warning(
                f"Слишком много запросов. Ждем {self.time_sleep_after_too_many_connection} секунд"
            )
            time.sleep(self.time_sleep_after_too_many_connection)
        else:
            time.sleep(self.time_sleep_between_connection)

    def _get_random_user_agent(self) -> str:
        """
        Возвращает случайный User-Agent из списка
        """
        return random.choice(USER_AGENTS)

    def get(self, url: str, **kwargs) -> httpx.Response:
        """
        GET-запрос

        :param url: URL для запроса
        :return: Ответ от сервера
        """
        headers = kwargs.pop("headers", {})
        headers["User-Agent"] = self._get_random_user_agent()
        logger.debug(f"GET {url=} with User-Agent: {headers['User-Agent']}")
        response = self.client.get(url, headers=headers, **kwargs)
        self._handle_rate_limit(response)
        return response

    def post(self, url: str, **kwargs) -> httpx.Response:
        """
        POST-запрос

        :param url: URL для запроса
        :return: Ответ от сервера
        """
        headers = kwargs.pop("headers", {})
        headers["User-Agent"] = self._get_random_user_agent()
        logger.debug(f"POST {url=} with User-Agent: {headers['User-Agent']}")
        response = self.client.post(url, headers=headers, **kwargs)
        self._handle_rate_limit(response)
        return response
