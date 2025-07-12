from django.contrib.auth import login, authenticate 
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password 
from settings_app.utils.email_notification import send_notification_to_old_email 


def reactiveted_account_disable(User, username, password):
    try:
        user = User.objects.get(username=username) 
    except User.DoesNotExist: 
        print("The account does not exist")
        return False 

    if check_password(password, user.password):
        if user.delete_at is not None and user.is_active is False:
            user.deleted_at=None 
            user.is_active=True 
            email = user.email
            user.save()

            subject="[Mythotomia] Votre compte à été réactivé" 
            templateEmailNotif = "emails/account_reactiveted_notification.html"
            templateEmailNotifTxt = "emails/account_reactiveted_notification.txt"
            notifResponse=send_notification_to_old_email(user, email, subject, templateEmailNotif, templateEmailNotifTxt)
            if notifResponse is not True:
                print("error to notification email send")
                return 2  
            else:
                return True 
        else: 
            print("The account is not temporary disable")
            return False 
    else:
        print("The password and identifiant does not match")
        return False 
    

def user_login(request, identifiant, password): 
    User = get_user_model()
    try: 
        user_obj = User.objects.get(email=identifiant)
    except User.DoesNotExist:
        try:
            user_obj = User.objects.get(username=identifiant)
        except User.DoesNotExist:
            return 2
        
    if '@' in identifiant:
        try:
            user_obj = User.objects.get(email=identifiant) 
            username = user_obj.username
        except User.DoesNotExist:
            username = None
    else:
        username = identifiant

    reactiveted_account_disable(User, username, password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user) 
        if not user.is_active:
            return 1

        return 0 
    else:
        return 2 
