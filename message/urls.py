from django.urls import path
from .views import message_add_view

urlpatterns = [
    path('', message_add_view,  name='message_add'),
]
