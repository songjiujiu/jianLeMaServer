#!/usr/bin/env python
"""Django 的命令行入口文件。

平时运行 `python manage.py runserver`、`python manage.py migrate`
这类命令时，都会先进入这个文件。
"""
import os
import sys


def main():
    # 告诉 Django：项目的配置文件在 jianlema_server/settings.py。
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jianlema_server.settings")
    from django.core.management import execute_from_command_line

    # 把命令行参数交给 Django 处理，例如 runserver、migrate、createsuperuser。
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    # 只有直接执行 manage.py 时才会调用 main()。
    main()
