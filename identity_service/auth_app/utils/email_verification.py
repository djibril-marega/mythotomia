from datetime import datetime, timezone
import random 
from django.db import connection 
from django.template.loader import render_to_string 
from auth_app.models import CustomUser, EmailVerification
from string import Template 
from django.conf import settings 

def generate_6_digit_code():
    digit_code=random.randint(100000, 999999)
    return str(digit_code) 

def register_email_verification_db(username, email, code): 
    if username is None:
        return "Username is not provided."
    if email is None:
        return "Email is not provided."
    if code is None:
        return "Code is not provided."
    
    # Check if the username already exists in the database 
    if not CustomUser.objects.filter(username=username).exists():
        return "Username not exists."
    
    # check if the email already exists and verified in the database
    if CustomUser.objects.filter(email=email).exclude(email_verified_at=None).exists(): 
        return "Email already verified."

    # Obtain userId from the database
    try:
        user=CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist: 
        return "User not found in the database."
    
    # Create a new email verification record 
    try:
        EmailVerification.objects.create(user=user, email=email, token=code)
    except Exception as e:
        return f"An error occurred while creating the email verification record: {str(e)}"
    
    # Check if the email verification record was created successfully
    if EmailVerification.id is None:
        return "Failed to create email verification. Please try again." 
    else: 
        return True


def load_email_template(code, username, tempatePath): 
    if username is None:
        return "Username is not provided."
    if code is None:
        return "Code is not provided."
    
    try:
        with open(tempatePath, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Email template file not found at {tempatePath}. Please check the file path.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the email template: {str(e)}")

    template = Template(html)
    try:
        html_message = template.safe_substitute(user_name=username, confirmation_code=code)
    except KeyError as e:
        raise KeyError(f"Missing placeholder in the template: {str(e)}. Please ensure 'user_name' and 'confirmation_code' are present in the template.")
    except Exception as e:
        raise Exception(f"An error occurred while substituting placeholders in the template: {str(e)}")
    
    return html_message


def send_verification_email(recipientEmail, code, username, ses_client, tempatePath): 
    # connect to AWS SES
    SENDER = settings.DEFAULT_FROM_EMAIL 
    SUBJECT = "Votre code de vérification"
    CHARSET = "UTF-8"
    
    try:
        templateEmail=load_email_template(code, username, tempatePath)
    except Exception as e:
        return f"An error occurred while loading the email template: {str(e)}"
    
    BODY_HTML = templateEmail
    BODY_TEXT = f"Votre code est : {code}"


    try:
        response = ses_client.send_email(
            Destination={'ToAddresses': [recipientEmail]},
            Message={
                'Body': {
                    'Html': {'Charset': CHARSET, 'Data': BODY_HTML},
                    'Text': {'Charset': CHARSET, 'Data': BODY_TEXT},
                },
                'Subject': {'Charset': CHARSET, 'Data': SUBJECT},
            },
            Source=SENDER, 
        )
    except Exception as e:
        return f"An error occurred while sending the email: {str(e)}"
    
    return response 


def verification_email_send_process(username, email, ses_client, templatePath):
    if ses_client is None:
        return "AWS SES client is not established."
    if username is None:
        return "Username is not provided."
    if email is None:
        return "Email is not provided."
    code = generate_6_digit_code()
    registrationStatus=register_email_verification_db(username, email, code) 
    if registrationStatus != True:
        return registrationStatus 
    
    response = send_verification_email(email, code, username, ses_client, templatePath)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200: 
        return True
    else:
        return "Failed to send verification email."
    


def verify_email_code(code, request, ses_client):
    if ses_client is None:
        return "AWS SES client is not established."
    if code is None:
        return "Code is not provided."
    if request is None:
        return "Request is not provided." 
    
    userId = request.user.id
    if userId is None:
        return "User ID is not found in the session."
    
    # Fetch the last email verification record for the user 
    try:
        last_email_verification = EmailVerification.objects.filter(user_id=request.user).order_by('-id').first()
    except EmailVerification.DoesNotExist:
        return "No email verification found for this user."
    
    # Find attempts made by the user
    # If no attempts have been made, set attempts to 0
    nbAttempts = last_email_verification.attempts
    if nbAttempts is None:
        nbAttempts = 0
    elif nbAttempts >= 3:
        return "You have exceeded the maximum number of attempts. Please request a new code."
    
    # Increment the number of attempts
    last_email_verification.attempts = nbAttempts + 1 
    last_email_verification.save() 

    # Chack if the expiration time is not over 
    if last_email_verification.expires_at < datetime.now(timezone.utc):
        return "Code has expired. Please request a new code."
    
    # Check if the code matches
    if last_email_verification.token != code:
        return "Code does not match. Please check your email."
    
    # Update the validation time in email_verifications table
    last_email_verification.verified_at = datetime.now(timezone.utc)
    try:
        last_email_verification.save() 
    except Exception as e:
        return f"An error occurred while saving the email verification: {str(e)}"

    # Check if the same email exists and verified in the users table
    try:
        user = CustomUser.objects.filter(email=last_email_verification.email).first()
    except CustomUser.DoesNotExist:
        return "User not found in the database. Please try again."
    
    try:
        user = CustomUser.objects.get(id=userId)
        user.email = last_email_verification.email
        user.email_verified_at = datetime.now()
        user.save() 
    except CustomUser.DoesNotExist:
        return "User not found in the database. Please try again."

    userRefresh = CustomUser.objects.get(id=userId)
    if userRefresh.email == last_email_verification.email:
        if userRefresh.email_verified_at is not None:
            return True 
        else:
            return "Failed to update email in the users table. Please try again."   
    else:
        return "Failed to update email in the users table. Please try again."
    