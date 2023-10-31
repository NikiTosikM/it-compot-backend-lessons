from django.shortcuts import render

from blog.models import Post


def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/posts_list.html', {'posts': posts})

