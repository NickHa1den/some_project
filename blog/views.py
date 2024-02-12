import json
import random

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
from blog.utils import CategoryTagMixin


class HomePageView(CategoryTagMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-public']
    slug_field = 'slug'
    queryset = Post.published.all().order_by('-public')
    paginate_by = 6

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Главная'
        return context

    # def get_object(self, queryset=None):
    #     return get_object_or_404(Post, slug=self.kwargs[self.slug_field])


# class AllPostView(ListView):
#     model = Post
#     queryset = Post.published.all()
#     template_name = 'blog/posts_by_signed.html'
#     context_object_name = 'posts'
#     paginate_by = 6
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Все посты'


class PostDetailView(CategoryTagMixin, DetailView):
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
        similar_posts = list(similar_posts)  # Преобразуем QuerySet в список, чтобы применить shuffle
        random.shuffle(similar_posts)
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
        if form.instance.status == 1:
            messages.success(self.request, 'Добавлена новая запись')
        else:
            messages.success(self.request, 'Создан черновик')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить пост'
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
        return reverse_lazy('blog:drafts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление поста'
        context['next'] = self.request.GET.get('next', '')  # Получаем значение параметра 'next' из GET запроса
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'category_list'
    queryset = Category.objects.all()
    slug_field = 'slug'

    def get_object(self, queryset=None):
        return get_object_or_404(Category, slug=self.kwargs[self.slug_field])


class CategoryDetailView(CategoryTagMixin, ListView):
    model = Post
    template_name = 'blog/categories.html'
    paginate_by = 10

    def get_object(self, queryset=None):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return category

    def get_context_data(self, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        cat_posts = Post.objects.filter(category=category).order_by('-created')
        context = super().get_context_data(**kwargs)
        context['title'] = f'{category.name}'
        context['cat_posts'] = cat_posts
        context['category'] = self.get_object()
        return context


class PostsByTagListView(CategoryTagMixin, ListView):
    model = Post
    template_name = 'blog/tagged_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_object(self, queryset=None):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return tag

    def get_queryset(self, **kwargs):
        return Post.objects.filter(tags__slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['title'] = f'{tag.name}'
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
        queryset = (self.model.objects.annotate(
            rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
                    )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Результаты поиска: {self.request.GET.get("q")}'
        context['query'] = self.request.GET.get('q')
        return context


class PostsBySignedView(LoginRequiredMixin, CategoryTagMixin, ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 6
    login_url = 'accounts:login'
    template_name = 'blog/posts_by_signed.html'

    def get_queryset(self):
        authors = self.request.user.profile.following.values_list('id', flat=True)
        queryset = self.model.objects.filter(author__id__in=authors)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Посты от авторов, на которых вы подписаны'
        return context


class DraftsList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/drafts.html'
    login_url = 'accounts:login'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user, status=0).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drafts'] = self.get_queryset()
        context['title'] = f'Ваши черновики'
        return context


# class DraftsDetail(LoginRequiredMixin, DetailView):
#     model = Post
#     template_name = 'blog/drafts_details.html'
