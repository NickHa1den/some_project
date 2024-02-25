# Generated by Django 5.0.1 on 2024-02-10 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_remove_profile_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=models.SlugField(blank=True, default=1, max_length=255, verbose_name='Для адресной строки'),
        ),
    ]
