from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import signupForm, loginForm, EmailVerificationForm
from django.contrib.auth import login, logout  
from django.db import IntegrityError
from django.contrib import messages
from django.conf import settings 
from django.contrib.auth.decorators import login_required 
from .utils.email_verification import verification_email_send_process, verify_email_code 
from .utils.connection import establish_ses_connection 
from .utils.login import user_login 
from django.urls import reverse 
from .utils.token_generate import generate_token 
import time 
from django.http import JsonResponse



# Create your views here.
def signup_view(request):
    vaultUrl=settings.VAULT_ADDR 
    vaultToken=settings.VAULT_TOKEN
    secretAwsPath=settings.VAULT_PATH_AWS_IAM
    mountPoint=settings.VAULT_MOUNT_POINT  
    ses_client=establish_ses_connection(vaultUrl, vaultToken, secretAwsPath, mountPoint)

    if request.method == "POST":
        form = signupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                username = form.cleaned_data.get("username")
                email = form.cleaned_data.get("email")  
                sendResult=verification_email_send_process(username, email, ses_client, templatePath="auth_app/templates/auth/email_confirmation_template-fr.html")
                if sendResult is True: 
                    messages.success(request, "Un code de vérification a été envoyé à votre adresse e-mail. Veuillez le vérifier.")
                    return redirect('verify-email')
                else:
                    messages.error(request, "Erreur lors de l'envoi du code de vérification. Veuillez réessayer.")
                    return redirect('signup')
            except IntegrityError:
                form.add_error(None, "Un utilisateur avec ce nom d'utilisateur ou cette adresse e-mail existe déjà.") 
            except Exception as e:
                form.add_error(None, f"Une erreur s'est produite lors de l'inscription : {str(e)}")
    else:
        form = signupForm()
    return render(request, "auth/signup.html", {"form": form})


@login_required
def verifyEmail_view(request):
    vaultUrl=settings.VAULT_ADDR 
    vaultToken=settings.VAULT_TOKEN 
    secretAwsPath=settings.VAULT_PATH_AWS_IAM
    mountPoint=settings.VAULT_MOUNT_POINT  
    ses_client=establish_ses_connection(vaultUrl, vaultToken, secretAwsPath, mountPoint)
    username = request.user.username
    email = request.user.email 
    form = None 
    if request.method == "POST":
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get("code") 
            success = verify_email_code(code, request, ses_client)
            context = {"form": form, 
                   "form_action_url":reverse('verify-email'), 
                   "resend_email_url":f"{reverse('verify-email')}?resend=1"}

            if success is True: 
                messages.success(request, "Email vérifié avec succès !")
                logout(request) 
                return redirect('login')
            else:
                form.add_error("code", "Code invalide, veuillez réessayer.")
                return render(request, "auth/verify_email_form.html" , context)
        else:
            context = {"form": form, 
                   "form_action_url":reverse('verify-email'), 
                   "resend_email_url":f"{reverse('verify-email')}?resend=1"}
            form.add_error("code", "Veuillez corriger les erreurs dans le formulaire.")
            return render(request, "auth/verify_email_form.html", context)

    elif request.method == "GET":
        # Handling code resending if the resend parameter is present in the URL.
        form = EmailVerificationForm()
        context = {"form": form, 
                   "form_action_url":reverse('verify-email'), 
                   "resend_email_url":f"{reverse('verify-email')}?resend=1"}
        
        if request.GET.get('resend') == '1':
            try:
                verification_email_send_process(username, email, ses_client, templatePath="auth_app/templates/auth/email_confirmation_template-fr.html")  # ta fonction d'envoi
                messages.success(request, "Un nouveau code a été envoyé à votre adresse mail.")
            except Exception:
                messages.error(request, "Erreur lors de l'envoi du code, veuillez réessayer.")
            return redirect('verify-email')

        return render(request, "auth/verify_email_form.html", context)  



def login_view(request):
    form = None
    RSAKeyName=settings.RSA_KEY_NAME
    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            identifiant = form.cleaned_data.get('identifiant')
            password = form.cleaned_data.get('password')
            result=user_login(request, identifiant, password)
            if result == 0:
                if request.user.email_verified_at is None:
                    messages.error(request, "Veuillez vérifier votre email avant de vous connecter.")
                    return redirect('verify-email')
                user = request.user
                header = {
                    "alg": "RS256",
                    "typ": "JWT"
                }

                playload = {
                    "sub": user.id,
                    "email": user.email,
                    "username": user.username, 
                    "email_verified": user.email_verified_at.isoformat(),
                    "role": user.role,
                    "iat": int(time.time()),
                    "exp": int(time.time())+86400,
                    "iss": "identity-service"
                }
                token=generate_token(header, playload, RSAKeyName) 
                response = JsonResponse({"message": "Token stored in cookie."})
                response.set_cookie(
                    key="access_token",
                    value=token,
                    httponly=True,  # XSS protection
                    secure=False,    # send only https connection
                    samesite='Strict', # ou 'Strict' pour + de sécurité (ou 'None' si en cross-domain avec HTTPS)
                    max_age=3600*24,   # cookie lifespan in seconds
                    path="/",       # cookie access all domain 
                )
                return response
            elif result == 1:
                messages.error(request, "Votre compte n'est pas actif. Veuillez vérifier votre email.")
                return redirect('verify-email')
            elif result == 2:
                form.add_error(None, "Identifiant ou mot de passe incorrects. Veuillez réessayer.") 
    else:
        form = loginForm()

    return render(request, 'auth/login.html', {'form': form})


