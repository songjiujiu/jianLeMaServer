# jianlemaSever

Python Django 服务端项目骨架。

## 技术选型

```text
后端框架：Django
API 框架：Django REST Framework
数据库：MySQL（远程环境），SQLite（本地默认兜底）
缓存：Redis（远程环境），本地内存缓存（未配置 Redis 时兜底）
鉴权：微信 OpenID + JWT
后台管理：Django Admin
oos +  ECS
```
## 学习路径
```text
第一阶段：先跑起来
目标：知道一个 Django 服务怎么启动、请求怎么进来。
你先掌握这些命令：
powershell



.\.venv\Scripts\activate
python manage.py runserver 127.0.0.1:8000
python manage.py test
python manage.py makemigrations
python manage.py migrate

然后打开：
text



GET /api/health/
GET /api/check-ins/today/
POST /api/check-ins/today/
POST /api/auth/wechat-login/

你要理解的链路是：
text



前端请求
-> urls.py 匹配路由
-> views.py 处理业务
-> models.py 操作数据库
-> Response 返回 JSON

这对前端工程师很友好，因为你可以把 Django view 理解成“后端版的接口 handler”。
第二阶段：按文件学
你这个项目核心文件很少，学习顺序建议：
manage.py
先知道它是 Django 命令入口。

jianlema_server/settings.py
学配置：数据库、JWT、Redis、环境变量、时区、Django app 注册。

jianlema_server/urls.py 和 api/urls.py
学路由怎么分发。

api/models.py
学 ORM：表、字段、外键、一对一、唯一约束。

api/views.py
学接口：参数、鉴权、数据库查询、事务、返回 JSON。

第三阶段：用小需求练手
不要只看代码。你应该一边学一边加功能。建议按这个顺序做：
新增“目标列表接口”
GET /api/goals/ 返回当前用户的目标列表。

新增“创建目标接口”
POST /api/goals/ 创建一个目标。

新增“删除或停用目标接口”
不真删数据，把 is_active=False。

新增“打卡历史接口”
GET /api/check-ins/ 支持按日期分页查询。

新增测试
用 api/tests.py 测健康检查、目标创建、打卡逻辑。

这几个需求做完，你就已经摸到后端核心了：路由、鉴权、ORM、业务规则、测试、数据库迁移。
第四阶段：连接前端
你是前端转全栈，这一步很重要。
你要练：
text

前端登录微信
-> 拿 code
-> 请求 /api/auth/wechat-login/
-> 保存 access token
-> 后续请求带 Authorization: Bearer xxx
-> 调用目标/打卡接口

这时你会真正理解 JWT、登录态、接口错误码、跨端数据流。
第五阶段：部署和服务器
你项目里已经有：
text

Dockerfile
docker-compose.yml
gunicorn
whitenoise
MySQL
Redis

部署学习顺序：
本地 SQLite 跑通。
本地 Docker 启 MySQL、Redis。
Django 切到 MySQL。
服务器安装 Docker。
上传项目或 git pull。
配 .env。
docker compose up -d --build。
配 Nginx 反向代理。
配域名和 HTTPS。
你作为前端，最需要补的后端观念是这几个：
text

HTTP 请求生命周期
数据库建模
ORM 查询
身份认证
环境变量
日志
部署
错误处理
测试
建议你接下来就从“目标接口”开始。我可以直接带你做第一步：在这个项目里新增 GET /api/goals/ 和 POST /api/goals/，一边写一边解释每一行为什么这么写。
```
## 当前目录说明

| 路径 | 说明 |
| --- | --- |
| `README.md` | 项目说明文档，包含目录说明、启动方式和接口说明。 |
| `requirements.txt` | Python 依赖列表，当前包含 Django、DRF、SimpleJWT、python-dotenv、requests、PyMySQL、django-redis。 |
| `.gitignore` | Git 忽略规则。 |
| `.env` | 本地环境变量文件，包含 Django 和微信小程序配置，不建议提交。 |
| `.env.example` | 环境变量示例文件，用于说明需要配置的变量。 |
| `manage.py` | Django 命令行入口，用于启动服务、执行迁移、运行测试等。 |
| `db.sqlite3` | 本地兜底开发数据库，由 `migrate` 命令生成。远程环境使用 MySQL。 |
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

## 远程 MySQL 和 Redis 配置

项目提供了 `docker-compose.yml`，可以统一启动本地 MySQL 和 Redis。先确认 `.env` 中包含下面这些变量：

```env
MYSQL_ROOT_PASSWORD=replace-with-root-password
MYSQL_DATABASE=jianlema
MYSQL_USER=jianlema
MYSQL_PASSWORD=replace-with-app-db-password

DB_ENGINE=mysql
DB_NAME=jianlema
DB_USER=jianlema
DB_PASSWORD=replace-with-app-db-password
DB_HOST=127.0.0.1
DB_PORT=3306

REDIS_PASSWORD=replace-with-redis-password
REDIS_URL=redis://:replace-with-redis-password@127.0.0.1:6379/0
REDIS_KEY_PREFIX=jianlema
```

启动 MySQL 和 Redis：

```powershell
docker compose up -d
```

查看容器状态和日志：

```powershell
docker compose ps
docker compose logs -f mysql
docker compose logs -f redis
```

首次启动后执行依赖安装和数据库迁移：

```powershell
pip install -r requirements.txt
py manage.py migrate
py manage.py runserver 127.0.0.1:8000
```

停止容器：

```powershell
docker compose down
```

如果需要清空本地 MySQL 和 Redis 数据，先停止容器，再删除 `docker-data/` 目录。

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
