from django.urls import path
from .views import HomePageView, PostDetailView, AddPostView, UpdatePostView, DeletePostView, \
    like_view, CategoryListView, CategoryDetailView, AddCategoryView

app_name = 'blog'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_details'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('post/edit/<slug:slug>/', UpdatePostView.as_view(), name='update_post'),
    path('post/<slug:slug>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('like/<int:pk>/', like_view, name='like_post'),
]
