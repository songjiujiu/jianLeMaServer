# jianlemaSever

Python Django 服务端项目骨架。

## 技术选型

```text
后端框架：Django
API 框架：Django REST Framework
数据库：SQLite（当前开发环境）
鉴权：微信 OpenID + JWT
后台管理：Django Admin
oos +  ECS
```

## 当前目录说明

| 路径 | 说明 |
| --- | --- |
| `README.md` | 项目说明文档，包含目录说明、启动方式和接口说明。 |
| `requirements.txt` | Python 依赖列表，当前包含 Django、DRF、SimpleJWT、python-dotenv、requests。 |
| `.gitignore` | Git 忽略规则。 |
| `.env` | 本地环境变量文件，包含 Django 和微信小程序配置，不建议提交。 |
| `.env.example` | 环境变量示例文件，用于说明需要配置的变量。 |
| `manage.py` | Django 命令行入口，用于启动服务、执行迁移、运行测试等。 |
| `db.sqlite3` | 本地开发数据库，由 `migrate` 命令生成。 |
| `api/` | Django 应用目录，用于编写业务接口、模型、测试等。 |
| `api/views.py` | API 视图文件，当前包含健康检查、微信登录、今日打卡接口。 |
| `api/urls.py` | API 路由文件，注册 API 接口地址。 |
| `api/tests.py` | API 测试文件，当前包含健康检查接口测试。 |
| `api/models.py` | 数据模型文件，当前包含用户资料、目标、每日打卡、连续打卡模型。 |
| `api/admin.py` | Django 管理后台注册文件，当前已注册业务模型。 |
| `api/apps.py` | Django 应用配置文件。 |
| `api/migrations/` | 数据库迁移文件目录。 |
| `jianlema_server/` | Django 项目配置目录。 |
| `jianlema_server/settings.py` | 项目核心配置，包括数据库、应用注册、时区、语言等。 |
| `jianlema_server/urls.py` | 项目总路由入口，当前挂载后台和 API 路由。 |
| `jianlema_server/asgi.py` | ASGI 服务入口，用于异步服务部署。 |
| `jianlema_server/wsgi.py` | WSGI 服务入口，用于常规 Python Web 服务部署。 |
| `.idea/` | PyCharm IDE 配置目录。 |
| `__pycache__/` | Python 编译缓存目录，可删除，不需要提交到版本库。 |

## 启动

Windows PowerShell 环境推荐使用 `py`：

```powershell
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
py manage.py migrate
py manage.py runserver 127.0.0.1:8000
```

如果你的环境中 `python` 命令可用，也可以使用：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

## 接口

| 方法 | 地址 | 说明 |
| --- | --- | --- |
| `GET` | `/api/health/` | 服务健康检查。 |
| `POST` | `/api/auth/wechat-login/` | 微信登录，使用微信小程序 `code` 换取 OpenID 并返回 JWT。 |
| `GET` | `/api/check-ins/today/` | 查询今日打卡记录，需要 JWT。 |
| `POST` | `/api/check-ins/today/` | 创建或更新今日打卡，需要 JWT。 |
| `GET` | `/admin/` | Django 管理后台。 |

## 微信登录请求示例

```json
{
  "code": "wx-login-code",
  "nickname": "用户昵称",
  "avatar_url": "https://example.com/avatar.png"
}
```

## 今日打卡请求示例

请求头：

```text
Authorization: Bearer <access_token>
```

请求体：

```json
{
  "goal_id": 1,
  "note": "今天已完成"
}
```

## 常用命令

```powershell
py manage.py runserver 127.0.0.1:8000
py manage.py test
py manage.py makemigrations
py manage.py migrate
```
