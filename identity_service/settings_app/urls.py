from django.urls import path
from . import views
from .views import MyPasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views 
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('security/password_change/', MyPasswordChangeView.as_view(), name='password_change'),
    path(
        'security/password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='security/password_change_done.html'
        ),
        name='password_change_done'
    ),
    path('security/', views.change_auth_view, name='security_change'),
    path('security/change-email/verify-password/', views.verify_password_view, name='verify_password'),
    path('security/change-email/', views.change_email_view, name='change_email'),
    path('security/change-email/confirm-new-email/', views.confirm_new_email_view , name='confirm_new_email'), 
    #path('security/change-email/done/', views.change_email_done_view, name='change_email_done'),
    path('security/change-username/verify-password/', views.verify_password_view, name='verify_username_password'), 
    path('security/change-username/', views.change_username_view, name='change_username'), 
    path('account/logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('security/delete-account/confirm', views.confirm_disable_account_view, name='delete_account_confirm'),
    path('security/delete-account/', views.disable_account_view, name='delete_account'), 
     
]