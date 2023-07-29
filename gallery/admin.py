from django.contrib import admin
from gallery.models import *


@admin.register(GalleryPost)
class GalleryAdmin(admin.ModelAdmin):
    ...
