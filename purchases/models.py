from django.db import models
from account.models import *
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.db.models import Sum


class ChainOfStores(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=2000, blank=True, null=True)
    amountOfPurchases = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = ("ChainOfStores")
        verbose_name_plural = ("ChainOfStores")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ChainOfStores_detail", kwargs={"pk": self.pk})


class Shop(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    amountOfPurchases = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    chainOfStores = models.ForeignKey(ChainOfStores, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = ("Shop")
        verbose_name_plural = ("Shops")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Shop_detail", kwargs={"pk": self.pk})


class Goods(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    avgCost = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        verbose_name = ("Goods")
        verbose_name_plural = ("Goods")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Goods_detail", kwargs={"pk": self.pk})
