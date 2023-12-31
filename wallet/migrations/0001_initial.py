# Generated by Django 4.2.3 on 2023-07-27 10:15

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_profile_balance'),
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionCategory',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='wallet.transactioncategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionDocument',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('description', models.CharField(blank=True, max_length=2000, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('users', models.ManyToManyField(to='account.profile')),
            ],
            options={
                'verbose_name': 'Документ транзакции',
                'verbose_name_plural': 'Документы транзакций',
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=9)),
                ('share', models.BooleanField(default=False)),
                ('includedAccountBalance', models.BooleanField(default=True)),
                ('members', models.ManyToManyField(blank=True, null=True, to='account.profile')),
            ],
            options={
                'verbose_name': 'Кошелек',
                'verbose_name_plural': 'Кошельки',
            },
        ),
        migrations.CreateModel(
            name='WalletTransferRegister',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('receiver_wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_received', to='wallet.wallet')),
                ('sender_wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_sent', to='wallet.wallet')),
            ],
            options={
                'verbose_name': 'Перевод денежных средств',
                'verbose_name_plural': 'Переводы денежных средств',
            },
        ),
        migrations.CreateModel(
            name='TransactionsRegister',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('ex', 'expenses'), ('in', 'income')], max_length=2)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('goods_name', models.CharField(blank=True, max_length=150, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('totalPrice', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.transactioncategory')),
                ('goods', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='purchases.goods')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='purchases.shop')),
                ('transactionDocument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.transactiondocument')),
            ],
            options={
                'verbose_name': 'Регистр транзакции',
                'verbose_name_plural': 'Регистр транзакций',
            },
        ),
        migrations.AddField(
            model_name='transactiondocument',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.wallet'),
        ),
    ]
