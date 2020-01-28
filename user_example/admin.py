from django.contrib import admin
from .models import UserProfile, PostProfile
# Register your models here.
admin.site.register(UserProfile)

admin.site.register(PostProfile)