from django.db.models import Sum, Case, When, F, DecimalField, Q, Value
from django.db.models.functions import Cast, Coalesce
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete, m2m_changed
from django.dispatch import receiver
from wallet.models import *



@receiver([pre_save, post_save], sender=TransactionDocument)
def update_transaction_document(sender, instance, **kwargs):
    # Устанавливаем имя
    if not instance.name:
        transaction_document_count = TransactionDocument.objects.all().count() + 1
        instance.name = f'TD-{str(transaction_document_count).zfill(4)}'


@receiver([pre_save, post_save], sender=TransactionsRegister)
def update_transactions_register(sender, instance, **kwargs):
    # Устанавливаем имя
    instance.totalPrice = instance.price * instance.quantity

    if not instance.name:
        transaction_document_count = TransactionsRegister.objects.all().count() + 1
        instance.name = f'TR-{str(transaction_document_count).zfill(4)}'



@receiver([post_save, post_delete], sender=TransactionsRegister)
def sender_TransactionsRegister(sender, instance, **kwargs):


    transaction_document = instance.transactionDocument

    if transaction_document is None:
        return

    # Получение суммы всех транзакций, связанных с документом транзакций
    total_amount = transaction_document.transactionsregister_set.aggregate(
        total=Sum(
            F('totalPrice') * Case(
                When(status='in', then=1),
                When(status='ex', then=-1),
                default=0,
                output_field=DecimalField()
            )
        )
    )['total'] or 0

    transaction_document.amount = total_amount
    transaction_document.save()


    # Обновление суммы кошелька
    wallet = Wallet.objects.get(pk=transaction_document.wallet.pk)

    if wallet is None:
        return

    total_amount = wallet.transactiondocument_set.aggregate(
        balance=Sum(
            'amount',
            default=0,
            output_field=DecimalField()
        )
    )['balance'] or 0

    wallet.balance = total_amount
    wallet.save()


    # Обновление баланса пользователей
    members = wallet.members.all()
    for member in members:
       total_amount = member.wallet_set.filter(includedAccountBalance=True).aggregate(
           balance=Sum(
                'balance',
                default=0,
                output_field=DecimalField(),
                )
            )['balance'] or 0
       member.balance = total_amount
       member.save()


@receiver([post_save, post_delete], sender=TransactionDocument)
def sender_Wallet(sender, instance, **kwargs):

    wallet = instance.wallet

    if wallet is None:
        return

    total_amount = wallet.transactiondocument_set.aggregate(
        balance=Sum(
            'amount',
            default=0,
            output_field=DecimalField()
        )
    )['balance'] or 0

    wallet.balance = total_amount
    wallet.save()

    members = wallet.members.all()
    for member in members:
       total_amount = member.wallet_set.filter(includedAccountBalance=True).aggregate(
           balance=Sum(
                'balance',
                default=0,
                output_field=DecimalField(),
                )
            )['balance'] or 0

       member.balance = total_amount
       member.save()

@receiver([post_save, post_delete], sender=Wallet)
def sender_Wallet(sender, instance, **kwargs):

    members = instance.members.all()

    for member in members:
       total_amount = member.wallet_set.filter(includedAccountBalance=True).aggregate(
           balance=Sum(
                'balance',
                default=0,
                output_field=DecimalField(),
                )
            )['balance'] or 0

       member.balance = total_amount
       member.save()


@receiver([post_save, post_delete], sender=WalletTransferRegister)
def sender_WalletTransferRegister(sender, instance, **kwargs):

    sender_wallet = instance.sender_wallet
    receiver_wallet = instance.receiver_wallet
    amount_transfer = instance.amount


    sender_wallet.balance -= amount_transfer
    sender_wallet.save()
    receiver_wallet.balance += amount_transfer
    receiver_wallet.save()

    sender_wallet_members = sender_wallet.members.all()
    for member in sender_wallet_members:
       total_amount = member.wallet_set.filter(includedAccountBalance=True).aggregate(
           balance=Sum(
                'balance',
                default=0,
                output_field=DecimalField(),
                )
            )['balance'] or 0

       member.balance = total_amount
       member.save()

    receiver_wallet_members = receiver_wallet.members.all()
    for member in receiver_wallet_members:
       total_amount = member.wallet_set.filter(includedAccountBalance=True).aggregate(
           balance=Sum(
                'balance',
                default=0,
                output_field=DecimalField(),
                )
            )['balance'] or 0

       member.balance = total_amount
       member.save()