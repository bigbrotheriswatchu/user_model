
from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('registration/', register, name='register'),
    path('accounts/<int:pk>/profile/', profile, name='profile'),
    path('profile/<int:pk>/edit', profile_edit, name='profile_edit')
]
