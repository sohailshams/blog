from django.urls import path 
from .views import register_view, profile_view, profile_image_view, profile_update_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('profile/<str:username>', profile_view, name='profile'),
    path('profile/<str:username>/<uuid:profile_uuid>/', profile_image_view, name='profile-image'),
     path('profile/<str:username>/<uuid:profile_uuid>/edit', profile_update_view, name='profile-update'),
]
