from django.urls import path

from .views import dev_login
from .views import health_check
from .views import today_check_in
from .views import wechat_login
from .views import health_goals
from .views import create_health_goal
from .views import goals
# api 应用自己的路由表。
# 完整路径 = 项目总路由里的 /api/ + 这里配置的路径。
urlpatterns = [
    # GET /api/health/：服务健康检查。
    path("health/", health_check, name="health-check"),
    # goals
    path("goals/", goals, name="goals"),
    # post 请求
    path("create_health_goal/", create_health_goal, name="create_health_goal"),
    # POST /api/auth/wechat-login/：微信登录，返回 JWT token。
    path("auth/wechat-login/", wechat_login, name="wechat-login"),
    path("auth/dev-login/", dev_login, name="dev-login"),
    # GET/POST /api/check-ins/today/：查询或提交今日打卡。
    path("check-ins/today/", today_check_in, name="today-check-in"),
]
