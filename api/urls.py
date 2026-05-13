from django.urls import path

from .views import health_check
from .views import today_check_in
from .views import wechat_login


urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("auth/wechat-login/", wechat_login, name="wechat-login"),
    path("check-ins/today/", today_check_in, name="today-check-in"),
]
