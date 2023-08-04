from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from account.models import Profile
from wallet.forms import *
from wallet.serializers import TransactionCategorySerializer
from rest_framework import generics


@login_required
def wallet(request):
    user = request.user
    profile = user.profile
    balance = profile.balance

    transaction_document_form = TransactionDocumentForm()
    transactions_register_form = TransactionsRegisterForm()

    context = {
        'balance': balance,
        'transaction_document_form': transaction_document_form,
        'transactions_register_form': transactions_register_form
    }

    if request.method == 'POST':
        transaction_document_form = TransactionDocumentForm(request.POST)
        transactions_register_form = TransactionsRegisterForm(request.POST)

        if transaction_document_form.is_valid() and transactions_register_form.is_valid():
            transaction_doc = transaction_document_form.save(commit=False)
            transaction_doc.save()
            transactions_register_form.instance.transactionDocument = transaction_doc
            transactions_register_form.save()
            return redirect(reverse("wallet"))

    return render(request, template_name='wallet.html', context=context)

@login_required
def detail_wallets(request):
    user_wallets = Wallet.objects.filter(members=request.user.profile)
    context = {'wallets': user_wallets}
    return render(request, 'detail_wallets.html', context)

@login_required
def manage_wallet(request, wallet_uuid=None):

    if not request.user.profile.user:
        return redirect('detail_wallets')

    if wallet_uuid:
        instance = get_object_or_404(Wallet, uuid=wallet_uuid)
        old_balance = instance.balance
        is_update = True
    else:
        instance = None
        old_balance = 0
        is_update = False

    if request.method == 'POST':
        form = WalletForm(request.POST, instance=instance)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.members.add(request.user.profile)
            wallet.save()

            balance_difference = wallet.balance - old_balance

            if not is_update and balance_difference > 0:
                request.user.profile.balance += balance_difference
                request.user.profile.save()

            return redirect('detail_wallets')
    else:
        form = WalletForm(instance=instance)

    return render(request, 'manage_wallet.html', {'form': form, 'is_update': is_update})

@login_required
def delete_wallet(request, wallet_uuid):
    wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
    wallet.delete()
    return HttpResponseRedirect(reverse("detail_wallets"))

@login_required
def manage_transaction_category(request, pk=None):
    user = request.user.profile
    transaction_category = get_object_or_404(TransactionCategory, pk=pk, user=user) if pk else None

    if request.method == 'POST':
        form = TransactionCategoryForm(request.POST, instance=transaction_category)
        if form.is_valid():
            transaction_category = form.save(commit=False)
            transaction_category.user = user
            transaction_category.save()
            return redirect(transaction_category.get_absolute_url())
    else:
        form = TransactionCategoryForm(instance=transaction_category)

    return render(request, 'manage_transaction_category.html', {'form': form})



