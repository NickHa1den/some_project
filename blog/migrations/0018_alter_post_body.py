# Generated by Django 5.0.1 on 2024-02-10 15:56

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Полное описание'),
        ),
    ]
