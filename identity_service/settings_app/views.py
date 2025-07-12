from django.contrib.auth.views import PasswordChangeView
from .forms import verifyPasswordForm, ChangeEmailForm, ChangeUsernameForm 
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth import views as auth_views 
from django.conf import settings 
from auth_app.utils.email_verification import verification_email_send_process, verify_email_code 
from auth_app.utils.connection import establish_ses_connection 
from .utils.email_notification import send_notification_to_old_email 
from auth_app.forms import EmailVerificationForm 
from django.urls import reverse 
from django.contrib.auth import get_user_model
User = get_user_model() 
from django.utils import timezone


@login_required
def change_auth_view(request):
    username = request.user.username 
    email = request.user.email
    context = {
        "username":username,
        "email":email
    }

    return render(request, "security/change_auth_form.html", context) 



class MyPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'security/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        # Send an email after a successful password change
        response = super().form_valid(form)
        user = self.request.user 
        email = user.email  
        request = self.request 

        subject="[Mythotomia] Notification de changement de mot de passe"
        templatePwdNotif = "emails/security_change_password_notification.html"
        templatePwdNotifTxt = "emails/security_change_password_notification.txt"
        notifResponse=send_notification_to_old_email(user, email, subject, templatePwdNotif, templatePwdNotifTxt) 
        if notifResponse is not True:
            form.add_error(request, notifResponse) 
            return self.form_invalid(form) 
        
        return super().form_valid(form)
    


@login_required
def verify_password_view(request):
    if request.method == "GET":
        change_param = request.GET.get('change')
        if change_param:
            request.session['change'] = change_param

    if request.method == "POST":
        form = verifyPasswordForm(request.POST) 
        if form.is_valid():
            password = form.cleaned_data.get("password")
            user = authenticate(username=request.user.username, password=password)
            if user:
                request.session['password_verified'] = True 
                if request.session.get('change') == 'email':
                    return redirect("change_email")
                elif request.session.get('change') == 'username':
                    return redirect("change_username") 
                elif request.session.get('change') == 'state-account':
                    return redirect("delete_account_confirm")
            else:
                form.add_error(None, "Le mot de passe que vous avez entré est incorrect. Veuillez réessayer.") 
    else:
        form = verifyPasswordForm() 

    return render(request, "security/verify_password.html", {'form': form})  

@login_required
def change_email_view(request):
    vaultUrl=settings.VAULT_ADDR 
    vaultToken=settings.VAULT_TOKEN
    secretAwsPath=settings.VAULT_PATH_AWS_IAM
    mountPoint=settings.VAULT_MOUNT_POINT  
    ses_client=establish_ses_connection(vaultUrl, vaultToken, secretAwsPath, mountPoint)
    if not request.session.get('password_verified'):
        return redirect("verify_password")

    form = ChangeEmailForm() 
    if request.method == "POST":
        form = ChangeEmailForm(request.POST) 
        newEmail = request.POST.get("new_email")
        request.session['new_email'] = newEmail
        username = request.user.username 
        
        request.session['new_email'] = newEmail 
        user = request.user 

        # Sending the code to the new address
        templatePath = "settings_app/templates/emails/security_change_email.html"  
        verifResponse=verification_email_send_process(username, newEmail, ses_client, templatePath)
        if verifResponse is not True:
            messages.error(request, verifResponse)
            return redirect("change_email")

        # Notification to the old address
        subject="[Mythotomia] Notification de changement d'adresse e-mail"
        templateEmailNotif = "emails/email_change_notification.html"
        templateEmailNotifTxt = "emails/email_change_notification.txt"
        notifResponse=send_notification_to_old_email(user, newEmail, subject, templateEmailNotif, templateEmailNotifTxt)
        if notifResponse is not True:
            messages.error(request, notifResponse) 
            return redirect("change_email")
        
        messages.success(request, "Un e-mail de vérification a été envoyé à votre nouvelle adresse. Veuillez vérifier votre boîte de réception.") 

        del request.session['password_verified']
        return redirect("confirm_new_email")
    
    return render(request, "security/change_email_form.html", {'form': form}) 

@login_required
def confirm_new_email_view(request):
    vaultUrl=settings.VAULT_ADDR 
    vaultToken=settings.VAULT_TOKEN 
    secretAwsPath=settings.VAULT_PATH_AWS_IAM
    mountPoint=settings.VAULT_MOUNT_POINT  
    ses_client=establish_ses_connection(vaultUrl, vaultToken, secretAwsPath, mountPoint)
    username = request.user.username
    email = request.session.get('new_email')
    
    if request.method == "POST":
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get("code") 
            success = verify_email_code(code, request, ses_client)
            context = {"form": form, 
                   "form_action_url":reverse('confirm_new_email'), 
                   "resend_email_url":f"{reverse('confirm_new_email')}?resend=1"}

            if success is True: 
                messages.success(request, "Votre adresse nouvelle e-mail a été vérifiée avec succès !") 
                return redirect('security_change')
            else:
                messages.error(request, "Code invalide, veuillez réessayer.")
                return render(request, "auth/verify_email_form.html" , context)
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
            return render(request, "auth/verify_email_form.html", context)

    elif request.method == "GET":
        # Handling code resending if the resend parameter is present in the URL
        form = EmailVerificationForm()  
        context = {"form": form, 
                   "form_action_url":reverse('confirm_new_email'),
                   "resend_email_url":f"{reverse('confirm_new_email')}?resend=1"}
        
        if request.GET.get('resend') == '1':
            templatePath = "settings_app/templates/emails/security_change_email.html"
            try:
                verification_email_send_process(username, email, ses_client, templatePath)
                messages.success(request, "Un nouveau code a été envoyé à votre adresse mail.")
            except Exception:
                messages.error(request, "Erreur lors de l'envoi du code, veuillez réessayer.")
            return redirect('confirm_new_email')

        # Sinon affichage normal du formulaire
        return render(request, "auth/verify_email_form.html", context)
    
@login_required 
def change_username_view(request):
    if not request.session.get('password_verified'):
        return redirect("verify_password")

    if request.method == "POST":
        form = ChangeUsernameForm(request.POST)
        if form.is_valid(): 
            new_username = form.cleaned_data.get("new_username")
            user = request.user
            old_username=user.username
            email= user.email 
            
            if User.objects.filter(username=new_username).exists(): 
                messages.error(request, "Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")
                return render(request, "security/change_username_form.html", {'form': form})
            
            user.username = new_username 
            user.save()

            subject="[Mythotomia] Notification de changement de nom d'utilisateur" 
            templateEmailNotif = "emails/username_change_notification.html"
            templateEmailNotifTxt = "emails/username_change_notification.txt"
            notifResponse=send_notification_to_old_email(user, email, subject, templateEmailNotif, templateEmailNotifTxt, old_username) 
            if notifResponse is not True:
                messages.error(request, notifResponse)
                return render(request, "security/change_username_form.html", {'form': form})

            del request.session['password_verified']

            messages.success(request, "Votre nom d'utilisateur a été mis à jour avec succès.")
            return redirect('security_change')
    else:
        form = ChangeUsernameForm()
    
    return render(request, "security/change_username_form.html", {'form': form}) 

    
@login_required 
def confirm_disable_account_view(request):
    if not request.session.get('password_verified'):
        return redirect("verify_password")
    return render(request, 'security/confirm_disable_account.html') 

@login_required
def disable_account_view(request):
    if not request.session.get('password_verified'):
        return redirect("verify_password")
    
    if request.method == "POST":
        user = request.user
        user.is_active = False 
        user.delete_at = timezone.now()
        user.save()
        email = user.email
        # send notification email for account delete alert
        subject="[Mythotomia] Confirmation de suppression de votre compte" 
        templateEmailNotif = "emails/disable_account_notification.html"
        templateEmailNotifTxt = "emails/disable_account_notification.txt"
        notifResponse=send_notification_to_old_email(user, email, subject, templateEmailNotif, templateEmailNotifTxt)
        if notifResponse is not True:
            messages.error(request, notifResponse)  
        
        logout(request)
        return redirect('login') 
    else:
        return redirect('security_change')