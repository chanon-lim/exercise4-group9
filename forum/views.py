from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import SubmitForm, CommentForm
from django.http import HttpResponseForbidden


# Create your views here.
def forum(request):
    """
    Homepage for forum
    """
    posts = Post.objects.order_by('-updated_on')
    context = {
        'posts': posts,
    }
    return render(request, 'forum/forum.html', context)


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

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data['content']
            comment = Comment(post=post, user=request.user, content=content)
            comment.save()
            return redirect('post_detail', post_id)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'forum/post_detail.html', context)


def post_edit(request, post_id):
    """
    Edit a post, only same user can edit it
    """
    post = get_object_or_404(Post, pk=post_id)
    default_value = {
        'title': post.title,
        'content': post.content,
    }

    if post.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        submit_form = SubmitForm(request.POST)
        if submit_form.is_valid():
            post = submit_form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_detail', post_id=post.pk)
    submit_form = SubmitForm(initial=default_value)

    context = {
        'form': submit_form
    }
    # Use the post_create template for edit, may change later
    return render(request, 'forum/post_create.html', context)


def post_delete(request, post_id):
    """
    Delete a post, only same user can delete it
    """
    post = get_object_or_404(Post, pk=post_id)
    post.delete(request=request)
    return redirect('forum')


def comment_delete(request, comment_id):
    """
    Delete a comment, only same user can delete it
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete(request=request)
    post_id = comment.post.pk
    return redirect('post_detail', post_id)
