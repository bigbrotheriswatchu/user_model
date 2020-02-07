from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('registration/', register, name='register'),
    path('accounts/<int:pk>/profile/', profile, name='profile'),
    path('profile/<int:pk>/edit', profile_edit, name='profile_edit'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/like', PostLikeToggle.as_view(), name='like'),
    path('post/<int:pk>/edit', post_edit, name='post_edit'),
]
