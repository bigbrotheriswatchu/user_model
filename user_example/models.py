from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True )

    location = models.CharField(max_length=50)
    age = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    favorite_auths = models.CharField(max_length=300,)
    favorite_books = models.CharField(max_length=300,)
    favorite_quote = models.CharField(max_length=300)

    about_me = models.CharField(max_length=300,)

    def __str__(self):
        return self.user.username