from django.urls import path
from .views import wx_login
# api 应用自己的路由表。
# 完整路径 = 项目总路由里的 /api/ + 这里配置的路径。
urlpatterns = [
    # Post /api/auth/wx-login/ 微信登录
    path('auth/wx_login',wx_login, name='wx_login'),
]
