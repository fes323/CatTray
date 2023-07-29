from decimal import Decimal
from django.db.models import Sum, Case, When, F, DecimalField, Q, Value
from django.core.management.base import BaseCommand

from wallet.models import Profile, TransactionDocument, Wallet


class Command(BaseCommand):
    help = 'Обновление баланса пользователей на основе кошельков'

    def handle(self, *args, **options):
        profiles = Profile.objects.all()
        for profile in profiles:
            balance =  profile.wallet_set.filter(includedAccountBalance=True).aggregate(
                        balance=Sum(
                                    'balance',
                                    default=0,
                                    output_field=DecimalField(),
                                    )
                            )['balance'] or 0
            profile.balance = balance
            profile.save()

        self.stdout.write(self.style.SUCCESS('Баланс пользователей обновлен'))
