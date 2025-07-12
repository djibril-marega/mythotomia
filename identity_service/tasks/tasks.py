from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def purge_deleted_users():
    threshold = timezone.now() - timedelta(days=30)
    User.objects.filter(delete_at__lte=threshold).delete()
