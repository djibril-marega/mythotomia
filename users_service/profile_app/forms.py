from django import forms
from django.core.validators import RegexValidator
from file_manage.valid_type_file import validate_image_mimetype
from django.core.exceptions import ValidationError
import datetime

name_validator = RegexValidator(
    regex=r"^[A-Za-zÀ-ÖØ-öø-ÿ \-']+$",
    message="Seules les lettres, les accents, les tirets et les apostrophes sont autorisés."
)

bio_validator = RegexValidator(
    regex=r"^[^<>]{0,1000}$",
    message="La biographie ne peut pas contenir les caractères '<' ou '>'."
)

class ChangeProfile(forms.Form):
    first_name = forms.CharField(
        label="Prénom :",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre prénom'}),
        max_length=50,
        required=False,
        validators=[name_validator]
    )

    last_name = forms.CharField(
        label="Nom :",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom'}),
        max_length=50,
        required=False,
        validators=[name_validator]
    )

    bio = forms.CharField(
        label="Biographie :",
        widget=forms.Textarea(attrs={'placeholder': 'Racontez votre histoire', 'rows': 5}),
        max_length=1000,
        required=False,
        validators=[bio_validator]
    )

    birth_date = forms.DateField(
        label="Date de naissance :",
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=False
    )

    banner = forms.ImageField(
        label="Bannière",
        required=False,
        validators=[validate_image_mimetype]
    )

    photo = forms.ImageField(
        label="Photo de profil",
        required=False,
        validators=[validate_image_mimetype]
    )

    def clean_last_name(self):
        value = self.cleaned_data.get("last_name")
        if value:
            name_validator(value)
        return value
    
    def clean_first_name(self):
        value = self.cleaned_data.get("first_name")
        if value:
            name_validator(value)
        return value 
    
    def clean_bio(self):
        value = self.cleaned_data.get("bio")
        if value:
            bio_validator(value)
        return value 
    
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo in (None, ''):
            return None
        validate_image_mimetype(photo)
        return photo

    def clean_banner(self):
        banner = self.cleaned_data.get('banner')
        if banner in (None, ''):
            return None
        validate_image_mimetype(banner)
        return banner 
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        if birth_date in (None, ''):
            return None

        if not isinstance(birth_date, datetime.date):
            raise ValidationError("Veuillez entrer une date valide.")

        if birth_date > datetime.date.today():
            raise ValidationError("La date de naissance ne peut pas être dans le futur.")

        return birth_date

