# Generated by Django 4.2.3 on 2023-07-27 10:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_profile_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChainOfStores',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(blank=True, max_length=2000, null=True)),
                ('amountOfPurchases', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
            options={
                'verbose_name': 'ChainOfStores',
                'verbose_name_plural': 'ChainOfStores',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('amountOfPurchases', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('description', models.CharField(blank=True, max_length=2000, null=True)),
                ('chainOfStores', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='purchases.chainofstores')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
            options={
                'verbose_name': 'Shop',
                'verbose_name_plural': 'Shops',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('avgCost', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('description', models.CharField(blank=True, max_length=2000, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
            options={
                'verbose_name': 'Goods',
                'verbose_name_plural': 'Goods',
            },
        ),
    ]
