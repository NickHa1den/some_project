import uuid

from PIL import Image
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.urls import reverse

from modules.services.utils import unique_slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='accounts/avatar', default='default.png', blank=True, null=True)
    slug = models.SlugField(verbose_name='Для адресной строки', blank=True, max_length=255, unique=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', verbose_name='Подписки',
                                       blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'username': self.user})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
