from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payment.settings')

# 实例化Celery
app = Celery('payment', broker='redis://127.0.0.1:6379/0')

# 使用django的settings文件配置celery
app.config_from_object('django.conf:settings')

# Celery加载所有注册的应用
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
