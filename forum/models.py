from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponseForbidden
from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    image = models.ImageField(blank=True)
    bio = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return self.user.get_username()


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    like = models.ManyToManyField(User, blank=True, related_name='post_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return 'Post {} by {} on {}'.format(
            self.title,
            self.user.username,
            self.created_on,
        )

    def delete(self, request, *args, **kwargs):
        if self.user != request.user:
            return HttpResponseForbidden()
        else:
            super().delete(*args, **kwargs)


class Comment(models.Model):
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    like = models.ManyToManyField(
        User,
        blank=True,
        related_name='comment_like'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {} on {}'.format(
            self.content,
            self.user.username,
            self.created_on,
        )

    def delete(self, request, *args, **kwargs):
        if self.user != request.user:
            return HttpResponseForbidden()
        else:
            super().delete(*args, **kwargs)
