# Generated by Django 2.2.6 on 2020-01-28 21:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_example', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postprofile',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
