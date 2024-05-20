import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "line_591_notifications.settings")
app = Celery("line_591_notifications")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()