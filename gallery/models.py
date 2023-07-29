import uuid
from django.db import models
from blog.models import Post


class GalleryPost(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name="post_image")
    image = models.ImageField(upload_to='post_image/')
    image_title = models.BooleanField(default=False, verbose_name="Является обложкой?")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image}"
