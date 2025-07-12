from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
User = get_user_model()


username_validator = RegexValidator(
    regex=r'^[a-z0-9_]+$',
    message="Le nom d'utilisateur ne peut contenir que des lettres minuscules, des chiffres et des tirets bas (_)."
)
code_validator =RegexValidator(
    regex=r'^\d{6}$',   
    message="Le code de vérification doit être un nombre à 6 chiffres."
)
class signupForm(UserCreationForm):
    email = forms.EmailField(required=True , label="Adresse e-mail")
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=24,
        min_length=3,
        validators=[username_validator],
        help_text="Le nom d'utilisateur doit comporter au moins 3 caractères.",
        error_messages={
            "required": "Ce champ est obligatoire.",
            "max_length": "Le nom d'utilisateur ne peut pas dépasser 24 caractères.",
            "min_length": "Le nom d'utilisateur doit comporter au moins 3 caractères.",
            "invalid": "Le nom d'utilisateur ne peut contenir que des lettres minuscules, des chiffres et des tirets bas (_).",
        },  
    )

    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        help_text="",
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput,
        help_text="",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        help_texts = {field: "" for field in fields}
        labels = {
            "username": "Nom d'utilisateur",
            "email": "Adresse e-mail",
            "password1": "Mot de passe",
            "password2": "Confirmer le mot de passe", 
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un utilisateur avec cette adresse e-mail existe déjà.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Un utilisateur avec ce nom d'utilisateur existe déjà.")
        return username
    
class loginForm(forms.Form): 
    identifiant = forms.CharField(label="Nom d'utilisateur ou adresse email", max_length=150)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput) 


class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        label="Code de vérification",
        max_length=6,
        min_length=6,
        validators=[code_validator],
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        help_text="Entrez le code de vérification envoyé à votre adresse e-mail.",
        error_messages={
            "required": "Ce champ est obligatoire.",
            "invalid": "Le code de vérification doit être un nombre à 6 chiffres.",
            "max_length": "Le code de vérification doit comporter exactement 6 chiffres.",
            "min_length": "Le code de vérification doit comporter exactement 6 chiffres.",

        },
    )