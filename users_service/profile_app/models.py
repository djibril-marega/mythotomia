from django.db import models

# Create your models here.
class UserProfile(models.Model):
    # Primary key
    id = models.AutoField(primary_key=True)
    
    # Other DB infos
    external_user_id = models.IntegerField()  # id utilisateur dans l'autre base
    email = models.EmailField()
    username = models.CharField(max_length=150)
    
    banner = models.ImageField(upload_to='banners/', blank=True, default='banners/default-banner.jpg')
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, default='profiles/default-photo.png')
    
    last_name = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)

    class Meta:
        db_table = "user_profile"

    def __str__(self):
        return f"{self.username} ({self.email})"
    