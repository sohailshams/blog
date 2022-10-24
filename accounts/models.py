import uuid
from django.db import models


class Profile(models.Model):
    profile_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile.png')
    location = models.CharField(max_length=100, blank=True)
    user_role = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
