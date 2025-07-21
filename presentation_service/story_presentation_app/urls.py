from django.urls import path
from . import views

urlpatterns = [ 
    path('story/create/', views.create_story_view, name='story-create'),
    path('story/<int:id>/', views.story_view, name='story'),
]