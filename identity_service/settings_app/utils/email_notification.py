from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_notification_to_old_email(user, new_email, subject, templateEmailNotif, templateEmailNotifTxt, old_username=None):
    from_email = "djibril-marega@gmx.com"
    to_email = [user.email]

    # Text Brut version
    text_message = (templateEmailNotifTxt 
        .replace('{user}', user.username)
        .replace('{new_email}', new_email)
    )

    # HTML Version
    html_message = render_to_string(templateEmailNotif, {
        'user': user,
        'new_email': new_email,
        'old_username': old_username,
        'new_username': user.username
    })

    try: 
        send_mail(
            subject=subject,
            message=text_message,
            from_email=from_email,
            recipient_list=to_email,
            html_message=html_message,
        )
    except Exception as e:
        return f"An error occurred while sending the notification email: {str(e)}"
    return True
