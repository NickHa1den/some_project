from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from blog.models import Post, Category
from blog.forms import PostForm, EditForm
from blog.utils import TagMixin


class HomePageView(TagMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created']
    slug_field = 'slug'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_list = Category.objects.all()
        context['category_list'] = category_list
        context['title'] = 'Real Blog! | Главная'
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs[self.slug_field])


class PostDetailView(TagMixin, DetailView):
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


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Добавлена новая запись')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Real Blog! | Добавить пост'
        return context


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'blog/add_category.html'
    fields = ('name',)
    success_url = reverse_lazy('blog:home')


class UpdatePostView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'blog/update_post.html'
    login_url = 'accounts:login'
    success_message = 'Пост обновлен!'


class DeletePostView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    login_url = 'accounts:login'
    success_message = 'Пост удален'

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user})


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'category_list'
    queryset = Category.objects.all()
    slug_field = 'slug'

    def get_object(self, queryset=None):
        return get_object_or_404(Category, slug=self.kwargs[self.slug_field])


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


class PostsByTagListView(TagMixin, ListView):
    model = Post
    template_name = 'blog/tagged_posts.html'
    context_object_name = 'posts'

    def get_queryset(self, **kwargs):
        return Post.objects.filter(tags__slug=self.kwargs.get('slug'))


def like_view(request, slug):
    post = get_object_or_404(Post, slug=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blog:post_details', args=[str(slug)]))
