# Generated by Django 4.1.11 on 2024-02-13 17:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('message', models.CharField(blank=True, max_length=100)),
                ('receiverUser', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver_transaction', to=settings.AUTH_USER_MODEL)),
                ('senderUser', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender_transaction', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountNumber', models.IntegerField(blank=True, unique=True, validators=[django.core.validators.MinValueValidator(1001261015), django.core.validators.MaxValueValidator(9701132007)])),
                ('balance', models.FloatField(default=0)),
                ('accountType', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=100)),
                ('accountHolder', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='account_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
