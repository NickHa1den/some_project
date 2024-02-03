from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from taggit.managers import TaggableManager
from unidecode import unidecode


class Post(models.Model):
    STATUS = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано')
    )
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='Слаг', max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_posts', verbose_name='Автор')
    body = RichTextUploadingField(verbose_name='Полное описание', blank=True, null=True)
    created = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    snippet = models.CharField(verbose_name='Краткое описание', max_length=255)
    images = models.ImageField(verbose_name='Фотография', upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True, verbose_name='Лайки')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='category_posts',
                                 verbose_name='Категория')
    tags = TaggableManager(verbose_name='Метки')
    status = models.CharField(verbose_name='Статус', choices=STATUS, default='draft', max_length=20)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('blog:post_details', kwargs={'slug': self.slug})


class Category(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=255)
    slug = models.SlugField(verbose_name='Слаг', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

# class Comment(models.Model):
#     pass
