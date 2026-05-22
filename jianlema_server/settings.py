from pathlib import Path

from dotenv import load_dotenv
import os
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent
# 读取项目根目录下的 .env 文件，把里面的环境变量加载进来。
load_dotenv(BASE_DIR / ".env")

# Django 项目的密钥；线上环境必须换成更安全的随机字符串。
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-change-me-in-production")

# DEBUG=True 方便本地开发；线上环境应该设置为 False。
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"

# 允许访问后端的域名或 IP，多个值用英文逗号分隔。
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if host.strip()
]

# Django 会加载这里列出的应用。
INSTALLED_APPS = [
    # Django 自带后台、用户、会话等基础功能。
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Django REST Framework：用来写 JSON API。
    "rest_framework",
    # simplejwt：用 JWT token 做接口登录认证。
    "rest_framework_simplejwt",
    # 当前项目自己的业务应用。
    "api",
]

# 中间件会按顺序处理每一次请求和响应。
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 项目的总路由文件，所有 URL 入口从这里开始分发。
ROOT_URLCONF = "jianlema_server.urls"

# 模板配置。这个项目主要是 API，模板用得不多，但 Django 后台仍会用到。
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI 是传统 Python Web 服务器启动 Django 项目时使用的入口。
WSGI_APPLICATION = "jianlema_server.wsgi.application"

# 数据库配置：默认使用 SQLite；设置 DB_ENGINE=mysql 后连接远程 MySQL。
DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()

if DB_ENGINE == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME", ""),
            "USER": os.getenv("DB_USER", ""),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", ""),
            "PORT": os.getenv("DB_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

REDIS_URL = os.getenv("REDIS_URL", "")

if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": os.getenv("REDIS_KEY_PREFIX", "jianlema"),
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "jianlema-local-cache",
        }
    }

# Django 自带的密码强度校验规则。
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# 后台和系统默认语言。
LANGUAGE_CODE = "zh-hans"

# 项目时区。打卡日期会按中国时间计算。
TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

# True 表示数据库里存 UTC 时间，显示时再转换成本地时区。
USE_TZ = True

# 静态文件 URL 前缀，例如后台 CSS/JS。
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# 新建模型时默认使用 BigAutoField 作为自增主键。
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework 全局配置。
REST_FRAMEWORK = {
    # JSONRenderer 返回 JSON；BrowsableAPIRenderer 提供浏览器里的可视化调试页面。
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    # 默认使用 JWT 认证。需要登录的接口会检查请求头里的 Authorization。
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# JWT token 有效期配置。
SIMPLE_JWT = {
    # access token：前端访问接口时携带，有效期 7 天。
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    # refresh token：用来刷新 access token，有效期 30 天。
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}

# 微信小程序登录配置，从 .env 读取。
WECHAT_APPID = os.getenv("WECHAT_APPID", "")
WECHAT_SECRET = os.getenv("WECHAT_SECRET", "")
