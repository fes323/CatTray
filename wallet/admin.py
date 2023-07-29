from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from wallet.models import TransactionCategory, Wallet, TransactionDocument, TransactionsRegister, WalletTransferRegister


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    readonly_fields = ['uuid']


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    fields = ('uuid', 'name', 'members', 'balance', 'share', 'includedAccountBalance')
    filter_horizontal = ('members',)
    list_display = ('name', 'balance', 'share', 'includedAccountBalance')
    list_filter = ('share', 'includedAccountBalance')
    readonly_fields = ['uuid']

class TransactionsRegisterInline(admin.TabularInline):
    model = TransactionsRegister
    extra = 1

@admin.register(TransactionDocument)
class TransactionDocumentAdmin(admin.ModelAdmin):
    fields = ('name', 'users', 'wallet', 'description', 'amount', 'uuid')
    readonly_fields = ['date', 'uuid']
    list_display = ('name', 'wallet', 'amount', 'date')
    list_filter = ('wallet', 'date')
    filter_horizontal = ('users',)
    search_fields = ('name', 'uuid')
    inlines = [TransactionsRegisterInline]

    def save_formset(self, request, form, formset, change):
        # Если формсет является TransactionsRegisterInline, создаем связанный регистр транзакции
        if formset.model == TransactionsRegister:
            instances = formset.save(commit=False)
            for instance in instances:
                # Сохраняем экземпляр TransactionsRegister, связанный с сохраненным TransactionDocument
                instance.transactionDocument = form.instance
                instance.save()
        else:
            super().save_formset(request, form, formset, change)

@admin.register(TransactionsRegister)
class TransactionsRegisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'transactionDocument', 'status', 'shop', 'date', 'category', 'goods_name', 'price', 'quantity', 'totalPrice')
    list_filter = ('transactionDocument', 'status', 'shop', 'category', 'goods')
    readonly_fields = ['uuid']
    search_fields = ['uuid', 'name']

@admin.register(WalletTransferRegister)
class WalletTransferRegisterAdmin(admin.ModelAdmin):
    list_display = ('sender_wallet', 'receiver_wallet', 'amount', 'date')
    list_filter = ('sender_wallet', 'receiver_wallet')
    search_fields = ('sender_wallet__name', 'receiver_wallet__name')
    readonly_fields = ['uuid']