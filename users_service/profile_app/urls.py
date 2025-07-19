from django.urls import path
from . import views

urlpatterns = [ 
    path('users/<str:username>/', views.profile_view, name='profile'),
    path('me/edit/', views.profile_edit_view, name='profile-edit'),
]
