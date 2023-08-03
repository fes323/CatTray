from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from blog.models import *
from gallery.models import *


def blog_list(request):
    posts = Post.objects.filter(published=True).order_by('-created_at')
    tags = Tag.objects.filter(published=True)
    photo_for_slider = GalleryPost.objects.all()
    context = {
        'posts':posts,
        'tags':tags,
        'photo_for_slider':photo_for_slider
    }

    return render(request, template_name='blog_list.html', context=context)