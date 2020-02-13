from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('registration/', register, name='register'),
    path('accounts/<int:pk>/profile/', profile, name='profile'),
    path('profile/<int:pk>/edit', profile_edit, name='profile_edit'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/<int:pk>/like', PostLikeToggle.as_view(), name='like-toggle'),
    path('api/post/<int:pk>/like', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('post/<int:pk>/edit', post_edit, name='post_edit'),
    path('post/<int:pk>/delete', post_del, name='post_del'),
]
