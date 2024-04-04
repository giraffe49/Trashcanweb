from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置 Django 的 settings 模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easysort.settings')

# 创建 Celery 实例
app = Celery('easysort')

# 使用 Django 配置文件
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动加载任务
app.autodiscover_tasks()