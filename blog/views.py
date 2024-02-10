import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from taggit.models import Tag

from blog.models import Post, Category, Comment
from blog.forms import PostForm, EditForm, CommentForm
from blog.utils import TagMixin


class HomePageView(TagMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created']
    slug_field = 'slug'
    queryset = Post.published.all()
    paginate_by = 6

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

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        total_likes = post.total_likes()
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:4]
        context['title'] = f'{post.title}'
        context['total_likes'] = total_likes
        context['liked'] = liked
        context['similar_posts'] = similar_posts
        context['form'] = CommentForm
        return context


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

    def get_object(self, queryset=None):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return category

    def get_context_data(self, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        cat_posts = Post.objects.filter(category=category).order_by('-created')
        context = super().get_context_data(**kwargs)
        context['title'] = f'Real Blog! | {category.name}'
        context['cat_posts'] = cat_posts
        context['category'] = self.get_object()
        return context


class PostsByTagListView(ListView):
    model = Post
    template_name = 'blog/tagged_posts.html'
    context_object_name = 'posts'

    def get_object(self, queryset=None):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return tag

    def get_queryset(self, **kwargs):
        return Post.objects.filter(tags__slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Посты с меткой'
        context['tag'] = self.get_object()
        return context


def like(request):
    data = json.loads(request.body)
    id = data["id"]
    post = Post.objects.get(id=id)
    checker = None

    if request.user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            checker = 0
        else:
            post.likes.add(request.user)
            checker = 1

    likes = post.total_likes()

    info = {
        'check': checker,
        'num_of_likes': likes
    }

    return JsonResponse(info, safe=False)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    login_url = 'accounts:login'

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_invalid(self, form):
        if self.is_ajax():
            print(form.errors)
            return JsonResponse({'error': form.errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post_id = self.kwargs.get('pk')
        comment.author = self.request.user
        comment.parent_id = form.cleaned_data.get('parent')
        comment.save()

        if self.is_ajax():
            return JsonResponse({
                'is_child': comment.is_child_node(),
                'id': comment.id,
                'author': comment.author.username,
                'parent_id': comment.parent_id,
                'created': comment.created.strftime('%b %d, %Y в %H:%M'),
                'avatar': comment.author.profile.avatar.url,
                'content': comment.content,
                'get_absolute_url': comment.author.profile.slug
            }, status=200)
        return redirect(comment.post.get_absolute_url())

    def handle_no_permission(self):
        return JsonResponse({'error': 'Необходимо авторизоваться для добавления комментария'}, status=400)


class SearchView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 10
    allow_empty = True
    template_name = 'blog/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        search_vector = SearchVector('body', weight='B', config='russian') + \
                        SearchVector('title', weight='A', config='russian')
        search_query = SearchQuery(query)
        return (self.model.objects.annotate(
            rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
                )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Результаты поиска: {self.request.GET.get("q")}'
        return context
