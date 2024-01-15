from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from blog.models import Post, Category
from blog.forms import PostForm, EditForm
from blog.utils import PermissionRequiredMixin


class HomePageView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created']
    slug_field = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_menu = Category.objects.all()
        context['category_menu'] = category_menu
        context['title'] = 'Real Blog! | Главная'
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs[self.slug_field])


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'

    def get_context_data(self, **kwargs):
        category_menu = Category.objects.all()
        context = super().get_context_data(**kwargs)
        stuff = get_object_or_404(Post, slug=self.kwargs['slug'])
        total_likes = stuff.total_likes()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['category_menu'] = category_menu
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs['slug'])


class AddPostView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    slug_field = 'slug'

    def form_valid(self, form):
        # form.instance.slug = slugify(form.instance.title)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Real Blog! | Добавить пост'
        return context


class AddCategoryView(PermissionRequiredMixin, CreateView):
    model = Category
    template_name = 'blog/add_category.html'
    fields = ('name',)
    success_url = reverse_lazy('blog:home')


class UpdatePostView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'blog/update_post.html'


class DeletePostView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:home')


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'category_list'
    queryset = Category.objects.all()


class CategoryDetailView(ListView):
    model = Post
    template_name = 'blog/categories.html'

    def get_context_data(self, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        cat_posts = Post.objects.filter(category=category).order_by('-created')
        context = super().get_context_data(**kwargs)
        context['title'] = f'Real Blog! | {category.name}'
        context['cat_posts'] = cat_posts
        return context


def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blog:post_details', args=[str(pk)]))
