from django.contrib import admin

from django.contrib import admin
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'body')
    prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ('slug',)
