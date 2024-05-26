import os
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

    def get(self, url: str, **kwargs) -> httpx.Response:
        """
        GET-запрос

        :param url: URL для запроса
        :return: Ответ от сервера
        """
        logger.debug(f"GET {url=}")
        response = self.client.get(url, **kwargs)
        self._handle_rate_limit(response)
        return response

    def post(self, url: str, **kwargs) -> httpx.Response:
        """
        POST-запрос

        :param url: URL для запроса
        :return: Ответ от сервера
        """
        logger.debug(f"POST {url=}")
        response = self.client.post(url, **kwargs)
        self._handle_rate_limit(response)
        return response
