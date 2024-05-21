from django.http import HttpResponse
from django.views.generic import View

from News.logger import make_logger

logger = make_logger(name="news-views")


class HealthCheckView(View):
    """
    Класс для проверки доступности сервиса
    """

    def get(self, request, *args, **kwargs):
        logger.debug(
            f"Проверка доступности сервиса. IP-адрес: {request.META['REMOTE_ADDR']}"
        )
        return HttpResponse(status=200)
