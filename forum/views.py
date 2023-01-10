from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from taggit.models import Tag

from .forms import CommentForm, ProfileEditForm, SubmitForm, UserEditForm
from .models import Comment, Post


# ---------- Forum homepage ----------
def forum(request):
    """
    Homepage for forum
    """
    # Sort order for post
    order = request.GET.get('order_by')

    if order == 'latest_post':
        posts = Post.objects.order_by('-created_on')
    elif order == 'oldest_post':
        posts = Post.objects.order_by('created_on')
    elif order == 'most_recent_activity':
        posts = Post.objects.order_by('-comments__created_on', '-created_on')
    elif order == 'oldest_activity':
        posts = Post.objects.order_by('comments__created_on', 'created_on')
    elif order == 'most_like':
        posts = Post.objects.annotate(
            count=Count('like')
        ).order_by('-count')
    else:
        posts = Post.objects.order_by('-created_on')
    common_tags = Post.tags.most_common()[:5]

    context = {
        'posts': posts,
        'common_tags': common_tags,
    }
    return render(request, 'forum/forum.html', context)


def tag_view(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    # Filter posts by tag name
    posts = Post.objects.filter(tags=tag)
    common_tags = Post.tags.most_common()[:5]
    context = {
        'tag': tag,
        'posts': posts,
        'common_tags': common_tags,
    }

    return render(request, 'forum/forum.html', context)


# ---------- Post ----------
@login_required
def post_create(request):
    """
    Submit a new post
    """
    if request.method == 'POST':
        submit_form = SubmitForm(request.POST)
        if submit_form.is_valid():
            post = submit_form.save(commit=False)
            post.user = request.user
            post.save()
            # For saving tag
            submit_form.save_m2m()
            return redirect('post_detail', post_id=post.pk)
    submit_form = SubmitForm()

    context = {
        'form': submit_form
    }
    return render(request, 'forum/post_create.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm(initial={'user': request.user.pk})

    # Post a comment only if login
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data['content']
                comment = Comment(
                    post=post,
                    user=request.user,
                    content=content,
                )
                comment.save()
                return redirect('post_detail', post.pk)
        else:
            # Redirect to login page
            login_url = reverse('account_login') \
                + '?next={}'.format(request.path)
            return redirect(login_url)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'forum/post_detail.html', context)


@login_required
def post_delete(request, post_id):
    """
    Delete a post, only same user can delete it
    """
    post = get_object_or_404(Post, pk=post_id)
    post.delete(request=request)
    return redirect('forum')


@login_required
def post_like(request, post_id):
    """
    Like a post
    """
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        if not post.like.filter(id=request.user.id).exists():
            post.like.add(request.user)
            post.save()
            return render(
                request,
                'forum/post_like_area.html',
                context={'post': post}
            )
        else:
            post.like.remove(request.user)
            post.save()
            return render(
                request,
                'forum/post_like_area.html',
                context={'post': post},
            )


# ---------- Comment ----------
@login_required
def comment_delete(request, comment_id):
    """
    Delete a comment, only same user can delete it
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete(request=request)
    post_id = comment.post.pk
    return redirect('post_detail', post_id)


@login_required
def comment_like(request, comment_id):
    """
    Like a comment
    """
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_id)
        if not comment.like.filter(id=request.user.id).exists():
            comment.like.add(request.user)
            comment.save()
            return render(
                request,
                'forum/comment_like_area.html',
                context={'comment': comment},
            )
        else:
            comment.like.remove(request.user)
            comment.save()
            return render(
                request,
                'forum/comment_like_area.html',
                context={'comment': comment},
            )


# ---------- Profile ----------
@login_required
def profile(request):
    """
    User profile
    """
    return render(request, 'forum/profile.html')


@login_required
def profile_edit(request):
    """
    Edit user profile
    """
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(
            request.POST,
            instance=request.user.profile,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'プロフィールが編集されました')
            return redirect('profile')

    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'forum/profile_edit.html', context)
