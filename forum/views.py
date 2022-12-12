from django.http import Http404
from django.shortcuts import render, redirect
from .models import Post
from .forms import SubmitForm


# Create your views here.
def forum(request):
    posts = Post.objects.order_by('-updated_on')
    context = {
        'posts': posts,
    }
    return render(request, 'forum/forum.html', context)


def submit(request):
    """
    Submit a new post
    """
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('forum')
    form = SubmitForm()
    return render(request, 'forum/submit.html', {'form': form})


def detailed_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    # comments = Comment.objects
    context = {
        'post': post,
    }
    if post is not None:
        return render(request, 'forum/post.html', context)
    raise Http404('Post does not exist')
