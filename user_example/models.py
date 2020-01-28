from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    location = models.CharField(max_length=50)
    age = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    favorite_auths = models.CharField(max_length=300)
    favorite_books = models.CharField(max_length=300)
    favorite_quote = models.CharField(max_length=300)

    about_me = models.CharField(max_length=300)

    def __str__(self):
        return self.first_name + self.last_name


class PostProfile(models.Model):
    """Adding post on profile page"""

    book_author = models.CharField(max_length=100)
    book_name = models.CharField(max_length=100)
    book_review = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.book_author
