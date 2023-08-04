from django import forms
from wallet.models import *

class TransactionDocumentForm(forms.ModelForm):
    class Meta:
        model = TransactionDocument
        fields = ['name', 'users', 'wallet', 'description', 'amount']

class TransactionsRegisterForm(forms.ModelForm):
    class Meta:
        model = TransactionsRegister
        fields = ['name', 'transactionDocument', 'status', 'shop', 'category', 'goods_name', 'goods', 'price', 'quantity', 'totalPrice']
        
class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'balance', 'share', 'includedAccountBalance']

class TransactionCategoryForm(forms.ModelForm):
    class Meta:
        model = TransactionCategory
        fields = ['name', 'parent']
