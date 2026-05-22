```text
框架流程
Django REST Framework 接收请求
      ↓
查询数据库
      ↓
返回 JSON
      ↓
前端渲染页面
```

## 数据迁移命令

修改 `models.py` 后，先生成迁移文件：

```powershell
.\.venv\Scripts\python.exe manage.py makemigrations
```

再把迁移执行到数据库：

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

如果已经激活虚拟环境，也可以简写：

```powershell
python manage.py makemigrations
python manage.py migrate
```

## Docker 部署命令

构建并启动所有服务：

```powershell
docker compose up -d --build
```

查看容器状态：

```powershell
docker compose ps
```

查看后端日志：

```powershell
docker compose logs -f web
```

手动执行数据库迁移：

```powershell
docker compose exec web python manage.py migrate
```

停止服务：

```powershell
docker compose down
```
