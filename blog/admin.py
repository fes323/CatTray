from django.contrib import admin
from blog.models import *
from gallery.models import GalleryPost
from django.contrib.auth import get_user_model
from mptt.admin import DraggableMPTTAdmin

User = get_user_model()

class GalleryPostInline(admin.StackedInline):
    model = GalleryPost
    can_delete = False
    verbose_name_plural = 'Media'
    fk_name = 'post'


class CategoryBlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']

class PostAdmin(admin.ModelAdmin):
    inlines = (GalleryPostInline,)
    extra = 1
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = [
        'tags'
    ]
    list_display = ['title', 'category', 'created_at', 'published']
    list_filter = ['category', 'tags']
    search_fields = ['title', 'tags', 'category']


admin.site.register(
    CategoryBlog,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
    prepopulated_fields = {"slug": ("name",)},
    search_fields = ['name'],
)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
