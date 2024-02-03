from django.urls import path
from .views import HomePageView, PostDetailView, AddPostView, UpdatePostView, DeletePostView, \
    like_view, CategoryListView, CategoryDetailView, AddCategoryView, PostsByTagListView

app_name = 'blog'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('post/create/', AddPostView.as_view(), name='add_post'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_details'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('post/<slug:slug>/update/', UpdatePostView.as_view(), name='update_post'),
    path('post/<slug:slug>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('like/<slug:slug>/', like_view, name='like_post'),
    path('post/tags/<slug:slug>/', PostsByTagListView.as_view(), name='posts-by-tags'),
]
