from django.db import models
import os
import unicodedata
import re

def illustration_upload_to(instance, filename):
    # Séparation extension/nom
    base, ext = os.path.splitext(filename)
    
    # Normalisation ASCII
    normalized = unicodedata.normalize('NFKD', base)
    ascii_name = normalized.encode('ascii', 'ignore').decode('ascii')
    
    # Nettoyage caractères spéciaux
    clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', ascii_name)[:50]  # Limite la longueur
    
    # Nom final
    return f"illustrations/{instance.external_user_id}_{clean_name}{ext}"

class PresentationStory(models.Model):
    # Primary key
    id = models.AutoField(primary_key=True)
    
    # Other DB infos
    external_user_id = models.IntegerField()  # id utilisateur dans l'autre base
    email = models.EmailField()
    username = models.CharField(max_length=150)
    
    # Champ illustrations avec fonction de renommage
    illustrations = models.ImageField(
        upload_to=illustration_upload_to,  # Utilisation de la fonction
        blank=True, 
        null=True
    )
    
    title = models.CharField(max_length=150, blank=True)
    subtitle = models.CharField(max_length=150, blank=True, null=True)
    author = models.CharField(max_length=150, blank=True)
    genre = models.CharField(max_length=150, blank=True)
    release_date = models.DateField(blank=True, null=True)
    country_of_origin = models.CharField(max_length=150, blank=True)
    cast = models.CharField(max_length=150, blank=True, null=True)
    synopsis = models.TextField(blank=True)

    class Meta:
        db_table = "story"

    def __str__(self):
        return f"{self.username} ({self.email})"
