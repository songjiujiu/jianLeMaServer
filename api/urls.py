from django.urls import path

from .views import health_check
from .views import today_check_in
from .views import wechat_login


# api 应用自己的路由表。
# 完整路径 = 项目总路由里的 /api/ + 这里配置的路径。
urlpatterns = [
    # GET /api/health/：服务健康检查。
    path("health/", health_check, name="health-check"),
    # POST /api/auth/wechat-login/：微信登录，返回 JWT token。
    path("auth/wechat-login/", wechat_login, name="wechat-login"),
    # GET/POST /api/check-ins/today/：查询或提交今日打卡。
    path("check-ins/today/", today_check_in, name="today-check-in"),
]
