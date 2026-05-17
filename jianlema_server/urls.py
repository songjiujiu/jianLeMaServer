from django.contrib import admin
from django.urls import include, path


# 总路由表：浏览器或前端请求进来后，Django 会从这里匹配 URL。
urlpatterns = [
    # Django 自带后台管理页面，例如 /admin/。
    path("admin/", admin.site.urls),
    # 所有 /api/ 开头的请求，交给 api/urls.py 继续匹配。
    path("api/", include("api.urls")),
]
