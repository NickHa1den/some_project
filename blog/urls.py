from django.urls import path
from .views import HomePageView, PostDetailView, AddPostView, UpdatePostView, DeletePostView, \
    like, CategoryListView, CategoryDetailView, AddCategoryView, PostsByTagListView, CommentCreateView, SearchView

app_name = 'blog'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('posts/create/', AddPostView.as_view(), name='add_post'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post_details'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('posts/<slug:slug>/update/', UpdatePostView.as_view(), name='update_post'),
    path('posts/<slug:slug>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('like/', like, name='like'),
    path('posts/tags/<slug:slug>/', PostsByTagListView.as_view(), name='posts-by-tags'),
    path('posts/<int:pk>/comment/create/', CommentCreateView.as_view(), name='comment-create'),
    path('search/', SearchView.as_view(), name='search'),
]
