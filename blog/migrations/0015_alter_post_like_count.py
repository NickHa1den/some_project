# Generated by Django 5.0.1 on 2024-02-07 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like_count',
            field=models.BigIntegerField(blank=True, default=None, null=True, verbose_name='Количество лайков'),
        ),
    ]
