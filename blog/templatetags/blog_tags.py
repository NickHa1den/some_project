from django import template
from django.db.models import Count

from blog.models import Post

register = template.Library()


@register.inclusion_tag('blog/posts/latest_posts.html')
def show_latest_posts(count=4):
    latest_posts = Post.published.order_by('-public')[:count]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/posts/most_commented.html')
def get_most_commented_posts(count=4):
    most_commented_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return {'most_commented_posts': most_commented_posts}
