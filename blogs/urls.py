from django.urls import path
from .views import blog_list_view, blog_detail_view, blog_add_view, blog_edit_view

urlpatterns = [
    path('post/<int:post_pk>/edit/', blog_edit_view,  name='blog_edit'),
    path('post/new/', blog_add_view,  name='blog_add'),
    path('post/<int:post_pk>/', blog_detail_view,  name='blog_detail'),
    path('', blog_list_view, name='home'),
]
