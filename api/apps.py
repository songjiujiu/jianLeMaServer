from django.apps import AppConfig


class ApiConfig(AppConfig):
    # 这个应用里模型的默认自增主键类型。
    default_auto_field = "django.db.models.BigAutoField"
    # 当前 Django 应用的名字，对应 api 这个目录。
    name = "api"
