from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db.models import Sum
from wallet.models import Wallet, TransactionDocument

class Command(BaseCommand):
    help = 'Recalculates the balances of all wallets'

    def handle(self, *args, **options):
        # Get all wallets
        wallets = Wallet.objects.all()

        for wallet in wallets:
            # Get the total amount from transaction documents associated with the wallet
            total_amount = TransactionDocument.objects.filter(wallet=wallet).aggregate(sum_amount=Sum('amount'))['sum_amount'] or Decimal(0)

            # Update the wallet's balance
            wallet.balance = total_amount
            wallet.save()

        self.stdout.write(self.style.SUCCESS('Wallet balances recalculated successfully'))
