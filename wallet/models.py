import uuid
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum, Case, When, F, DecimalField, Q

from account.models import *
from purchases.models import *

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey



class TransactionCategory(MPTTModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name = ("Категория транзакции")
        verbose_name_plural = ("Категории транзакций ")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("TransactionCategory_detail", kwargs={"pk": self.pk})


class Wallet(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(Profile, null=True, blank=True)
    name = models.CharField(max_length=250)
    balance = models.DecimalField(max_digits=9, decimal_places=2, )
    share = models.BooleanField(default=False)
    includedAccountBalance = models.BooleanField(default=True)

    class Meta:
        verbose_name = ("Кошелек")
        verbose_name_plural = ("Кошельки")

    def __str__(self):
        return f"{self.name} ({self.members.first()})"

    def get_absolute_url(self):
        return reverse("Wallet_detail", kwargs={"pk": self.pk})


class WalletTransferRegister(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transfers_sent')
    receiver_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transfers_received')
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Перевод денежных средств"
        verbose_name_plural = "Переводы денежных средств"

    def __str__(self):
        return f"Перевод из {self.sender_wallet} в {self.receiver_wallet}"


class TransactionDocument(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, blank=True, null=True)
    users = models.ManyToManyField(Profile)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000, null=True, blank=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)

    class Meta:
        verbose_name = ("Документ транзакции")
        verbose_name_plural = ("Документы транзакций")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("TransactionDocument_detail", kwargs={"pk": self.pk})


class TransactionsRegister(models.Model):

    STATUS = [
        ('ex', 'expenses'),
        ('in', 'income')
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, blank=True, null=True)
    transactionDocument = models.ForeignKey(TransactionDocument, on_delete=models.CASCADE)

    status = models.CharField(choices=STATUS, max_length=2)

    shop = models.ForeignKey(Shop,on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    goods_name = models.CharField(max_length=150, blank=True, null=True)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    quantity = models.PositiveSmallIntegerField(default=1)
    totalPrice = models.DecimalField(max_digits=9, decimal_places=2, default=0)


    class Meta:
        verbose_name = ("Регистр транзакции")
        verbose_name_plural = ("Регистр транзакций")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("TransactionsRegister_detail", kwargs={"pk": self.pk})
