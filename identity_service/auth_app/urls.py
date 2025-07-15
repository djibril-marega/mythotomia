from django.urls import path
from .views import signup_view, verifyEmail_view, login_view   # Import the views
from django.contrib.auth import views as auth_views

urlpatterns = [ 
    path('signup/', signup_view, name='signup'),
    path('verify-email/', verifyEmail_view, name='verify-email'),  # Placeholder for email verification 
    path('login/', login_view, name='login'),  # Placeholder for login view 
    path(
        'reset-password/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/auth_password_reset_form.html',
            html_email_template_name ='registration/auth_password_reset_email.html',
            email_template_name='registration/auth_password_reset_email.txt',
            subject_template_name='registration/auth_password_reset_subject.txt'
        ),
        name='password_reset' 
    ),

    path(
        'reset-password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/auth_password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset-password-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/auth_password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset-password-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/auth_password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
