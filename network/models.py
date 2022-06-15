from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profile")
    follower = models.ManyToManyField(User, blank=True, related_name="follower_user")
    following = models.ManyToManyField(User, blank=True, related_name="following_user")
    avatar = models.CharField(max_length=180, default=None, blank=True, null=True)
    banner = models.CharField(max_length=180, blank=True, null=True, default=None)
    banner_side = models.CharField(max_length=180, blank=True, null=True, default=None)
    bio = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f'{self.user}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="user_posts", default=None)
    like = models.ManyToManyField(User, blank=True, related_name='like')
    comment = models.CharField(max_length=500, default=None, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'
