import uuid
from django.db import models


BLOG_USER_CHOICES = (
		('owner','Owner'),
		('viewer','Viewer'),
	)


class BlogPost(models.Model):
    post_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    auther = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=20, choices=BLOG_USER_CHOICES, default='owner')
    def __str__(self):
        return self.title
