from django.db import models

# Create your models here.
class UserProfile(models.Model):
    # Clé primaire locale
    id = models.AutoField(primary_key=True)
    
    # Infos provenant de l'autre base (auth)
    external_user_id = models.IntegerField()  # id utilisateur dans l'autre base
    email = models.EmailField()
    username = models.CharField(max_length=150)
    
    # Champs de profil
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    last_name = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.email})"