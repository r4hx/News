from django.contrib import admin
from django.urls import include, path

from News.views import HealthCheckView
from Rss.urls import urlpatterns as rss_urlpatterns
from Web.urls import urlpatterns as web_urlpatterns

urlpatterns = [
    path("healthz/", HealthCheckView.as_view(), name="health-checker"),
    path("rss/", include(rss_urlpatterns)),
    path("", include(web_urlpatterns)),
    path("admin/", admin.site.urls),
]
