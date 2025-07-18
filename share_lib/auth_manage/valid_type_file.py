import imghdr
from django.core.exceptions import ValidationError

def validate_image_mimetype(file):
    file.seek(0)  # Important : s'assurer qu'on lit depuis le début
    file_type = imghdr.what(file)
    if file_type not in ['jpeg', 'png']:
        raise ValidationError("Seules les images PNG et JPG sont autorisées.")
