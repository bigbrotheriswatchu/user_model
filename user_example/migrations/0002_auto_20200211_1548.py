# Generated by Django 2.1.2 on 2020-02-11 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_example', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='background_image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
