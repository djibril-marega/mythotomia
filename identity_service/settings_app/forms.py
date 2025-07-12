from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django import forms 
from django.core.validators import RegexValidator


class verifyPasswordForm(forms.Form):
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'placeholder': 'Entrez votre mot de passe'}),
        max_length=128,
        required=True,
        error_messages={
            'required': "Veuillez entrer votre mot de passe."  
        }
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError("Veuillez entrer votre mot de passe.")
        return password
    
class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(
        label="Nouvelle adresse e-mail",
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': 'Entrez votre nouvelle adresse e-mail'})
    )

    def clean_new_email(self):
        new_email = self.cleaned_data.get('new_email')
        if not new_email:
            raise ValidationError("Veuillez entrer une nouvelle adresse e-mail.")
        return new_email 


username_validator = RegexValidator(
    regex=r'^[a-z0-9_]+$',
    message="Le nom d'utilisateur ne peut contenir que des lettres minuscules, des chiffres et des tirets bas (_)."
)
class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(
        label="Nouveau nom d'utilisateur", 
        max_length=24,
        min_length=3,
        validators=[username_validator],
        help_text="Le nom d'utilisateur doit comporter au moins 3 caractères.",
        error_messages={
            "required": "Ce champ est obligatoire.",
            "max_length": "Le nom d'utilisateur ne peut pas dépasser 24 caractères.",
            "min_length": "Le nom d'utilisateur doit comporter au moins 3 caractères.",
            "invalid": "Le nom d'utilisateur ne peut contenir que des lettres minuscules, des chiffres et des tirets bas (_).",
        },)

    def clean_new_username(self):
        new_username = self.cleaned_data.get('new_username')
        if not new_username:
            raise ValidationError("Veuillez entrer un nouveau nom d'utilisateur.")
        return new_username  