import os
import time

import httpx

from News.logger import make_logger

logger = make_logger(name="tools-http")

HTTP_RESPONSE_TIMEOUT = os.getenv("HTTP_RESPONSE_TIMEOUT")
if HTTP_RESPONSE_TIMEOUT is None:
    raise Exception("HTTP_RESPONSE_TIMEOUT is not set")
HTTP_TIME_SLEEP_AFTER_TOO_MANY_CONNECTION = os.getenv(
    "HTTP_TIME_SLEEP_AFTER_TOO_MANY_CONNECTION"
)
if HTTP_TIME_SLEEP_AFTER_TOO_MANY_CONNECTION is None:
    raise Exception("HTTP_TIME_SLEEP_AFTER_TOO_MANY_CONNECTION is not set")
HTTP_TIME_SLEEP_BETWEEN_CONNECTION = os.getenv("HTTP_TIME_SLEEP_BETWEEN_CONNECTION")
if HTTP_TIME_SLEEP_BETWEEN_CONNECTION is None:
    raise Exception("HTTP_TIME_SLEEP_BETWEEN_CONNECTION is not set")


class HttpClient:
    """
    Класс для работы с HTTP
    """

    def __init__(
        self,
        timeout=int(HTTP_RESPONSE_TIMEOUT),
        time_sleep_after_too_many_connection=int(
            HTTP_TIME_SLEEP_AFTER_TOO_MANY_CONNECTION
        ),
        time_sleep_between_connection=int(HTTP_TIME_SLEEP_BETWEEN_CONNECTION),
        **kwargs,
    ):
        self.timeout = timeout
        self.time_sleep_after_too_many_connection = time_sleep_after_too_many_connection
        self.time_sleep_between_connection = time_sleep_between_connection
        self.client = httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            **kwargs,
        )

    def get(self, url, **kwargs):
        """
        GET-запрос
        """
        logger.debug(f"GET {url=}")
        response = self.client.get(url, **kwargs)
        if response.status_code == 429:
            time.sleep(int(self.time_sleep_after_too_many_connection))
        else:
            time.sleep(int(self.time_sleep_between_connection))
        return response

    def post(self, url, **kwargs):
        """
        POST-запрос
        """
        logger.debug(f"POST {url=}")
        response = self.client.post(url, **kwargs)
        if response.status_code == 429:
            time.sleep(int(self.time_sleep_after_too_many_connection))
        else:
            time.sleep(int(self.time_sleep_between_connection))
        return response
