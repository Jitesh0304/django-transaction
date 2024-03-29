# Generated by Django 4.1.11 on 2024-02-13 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_transactionmodel_accountnum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionmodel',
            name='accountNum',
        ),
        migrations.AddField(
            model_name='transactionmodel',
            name='receiveraccountNum',
            field=models.IntegerField(),
        ),
        migrations.AddField(
            model_name='transactionmodel',
            name='senderaccountNum',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='transactionmodel',
            name='amount',
            field=models.FloatField(),
        ),
    ]
