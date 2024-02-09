from django.contrib import admin

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Post, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'body')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'post', 'author', 'created')
    mptt_level_indent = 2
    list_display_links = ('post',)
    list_filter = ('created', 'updated', 'author')
