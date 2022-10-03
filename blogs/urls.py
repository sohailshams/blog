from django.urls import path
from .views import blog_list_view, blog_detail_view, blog_add_view, blog_edit_view, blog_delete_view

urlpatterns = [
    path('', blog_list_view, name='home'),
    path('posts/detail/<uuid:post_uuid>/', blog_detail_view,  name='blog_detail'),
    path('posts/new/', blog_add_view,  name='blog_add'),
    path('posts/<uuid:post_uuid>/edit/', blog_edit_view,  name='blog_edit'),
    path('posts/<uuid:post_uuid>/delete/', blog_delete_view,  name='blog_delete'),
]
