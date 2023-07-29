from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from blog.models import *


def blog_list(request):
    posts = Post.objects.filter(published=True).order_by('-created_at')
    tags = Tag.objects.filter(published=True)
    context = {
        'posts':posts,
        'tags':tags
    }

    return render(request, template_name='blog_list.html', context=context)