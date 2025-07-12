from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from datetime import timedelta


def get_expiration_date():
    return timezone.now() + timedelta(days=1)


# Create your models here.
class CustomUser(AbstractUser):
    name=models.CharField(max_length=150, null=True, default=None)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    email_verified_at=models.DateTimeField(null=True, default=None) 
    role=models.CharField(max_length=50, null=True, default=None)
    picture_profile=models.CharField(max_length=150, null=True, default=None) 
    last_update=models.DateTimeField(null=True, default=None)
    delete_at=models.DateTimeField(null=True, default=None) 
    created_at=models.DateTimeField(auto_now_add=True) 
    last_login=models.DateTimeField(null=True, default=None)
    is_staff=models.BooleanField(default=False) 
    is_superuser=models.BooleanField(default=False) 
    is_active=models.BooleanField(default=True)
    
    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
    
    groups = models.ManyToManyField(
        Group,
        related_name="users_in",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="users_in",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
        related_query_name="customuser",
    )


class EmailVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    token = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiration_date)
    verified_at = models.DateTimeField(null=True, default=None) 
    attempts = models.IntegerField(default=0) 
    
    class Meta:
        db_table = 'email_verifications'
    
    def __str__(self):
        return f"Email verification for {self.userId.username} - Token: {self.email}"

class LoginAttempt(models.Model):
    username = models.CharField(max_length=150, null=True, default=None) 
    email = models.EmailField(null=True, default=None) 
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    failure_reason = models.TextField(null=True, default=None)
    location = models.CharField(max_length=255, null=True, default=None)
    
    class Meta:
        db_table = 'login_attempts'
    
    def __str__(self):
        return f"Login attempt for {self.username} - Success: {self.success}"
