from django.contrib import admin
from .models import BlogPost, BlogComment, BlogLike

admin.site.register(BlogPost)
admin.site.register(BlogComment)
admin.site.register(BlogLike)
