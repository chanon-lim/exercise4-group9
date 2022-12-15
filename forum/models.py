from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    image = models.ImageField(blank=True)
    bio = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return self.user.get_username()


class Label(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label, blank=True)

    class Meta:
        ordering = ["-updated_on"]

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
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

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
