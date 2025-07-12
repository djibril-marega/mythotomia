# identity_service/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "identity_service.settings")

app = Celery("identity_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler' 

