from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from blog.models import Tag
from gallery.models import GalleryPost


def gallery(request):
    allPhoto = GalleryPost.objects.all().order_by('-uploaded_at')
    tags = Tag.objects.filter(published=True)
    context = {
        'allPhoto':allPhoto,
        'tags': tags,
    }
    return render(request, template_name='gallery.html', context=context)