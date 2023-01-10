from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponseForbidden
from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        blank=True,
        on_delete=models.CASCADE,
    )
    bio = models.TextField(max_length=300, default='こんにちは！')
    password = models.CharField(blank=True, max_length=32)

    def __str__(self):
        return str(self.user)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

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
    content = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)

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
