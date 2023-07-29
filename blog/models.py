from django.db import models
from django.urls import reverse
from account.models import *
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model


User = get_user_model()

class CategoryBlog(MPTTModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(unique=True, null=True, blank=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']

    class Meta:
        verbose_name = 'Категория блога'
        verbose_name_plural = 'Категории блога'

    def __str__(self):
        return self.name



class Tag(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    published = models.BooleanField(default=True, verbose_name='Отображать тег на сайте?')

    class Meta:
        verbose_name = ("Тег")
        verbose_name_plural = ("Теги")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Tag", kwargs={"pk": self.pk})


class Post(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(CategoryBlog, on_delete=models.CASCADE, verbose_name='Категория', null=True, blank=True, default=None)
    tags = models.ManyToManyField(Tag, null=True, blank=True, related_name="tags")
    text = models.TextField(max_length=10000, null=True,blank=True)
    published = models.BooleanField(default=True, verbose_name='Отображать пост на сайте?')

    class Meta:
        verbose_name = ("Пост")
        verbose_name_plural = ("Посты")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Post_detail", kwargs={"slug": self.slug})
