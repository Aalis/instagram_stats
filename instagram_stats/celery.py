from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from time import sleep

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instagram_stats.settings")

app = Celery("instagram_stats")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
