from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from pytils.translit import slugify
from taggit.managers import TaggableManager
from unidecode import unidecode
from modules.services.utils import unique_slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='Слаг', max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_posts', verbose_name='Автор')
    body = RichTextUploadingField(verbose_name='Полное описание', null=True, blank=True)
    # body = CKEditor5Field(verbose_name='Полное описание', config_name='extends', null=True, blank=True)
    created = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    snippet = models.CharField(verbose_name='Краткое описание', max_length=255)
    images = models.ImageField(verbose_name='Фотография', upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='like', blank=True, verbose_name='Лайки', default=None)
    like_count = models.BigIntegerField(verbose_name='Количество лайков', blank=True, null=True, default=None)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='category_posts',
                                 verbose_name='Категория')
    tags = TaggableManager(verbose_name='Метки')
    status = models.BooleanField(verbose_name='Статус', choices=Status.choices, max_length=20)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

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


class Comment(MPTTModel):
    post = models.ForeignKey(Post, verbose_name='Пост', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE,
                               related_name='comments_author')
    content = models.TextField(verbose_name='Текст комментария', max_length=3000)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True,
                            related_name='children', on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['-created', ]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return f'{self.author}: {self.content}'
