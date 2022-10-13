from django.contrib import admin
from .models import BlogPost, BlogComment

admin.site.register(BlogPost)
admin.site.register(BlogComment)
