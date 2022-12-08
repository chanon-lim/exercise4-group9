from django.shortcuts import render
from .models import Profile, Label, Post, Comment

# Create your views here.
def index(request):
    return render(request, 'forum/index.html')

def post_list(request):
    posts = Post.objects.order_by('-updated_on')
    context = {
        'posts': posts,
    }
    return render(request, 'forum/post_list.html', context)

def post(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects
    context = {
        'post': post,
    }
    return render(request, 'forum/post.html', context)