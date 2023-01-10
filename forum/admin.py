from django.contrib import admin

from forum.models import Comment, Post, Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = (
        "id",
        "title",
        "created_on",
    )
    list_filter = (
        "created_on",
    )
    list_editable = (
        "title",
    )
    search_fields = (
        "title",
        "content",
    )
    date_hierarchy = "created_on"
    save_on_top = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
