import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(
        ("phone"),
        region="RU",
        max_length=15,
        blank=True,
        null=True,
        unique=True,
        help_text=(
            "Номер телефона необходимо вводить в международном формате: +7.\nНомер должен быть уникальным"
        ),
    )
    bio = models.TextField(max_length=5000, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()