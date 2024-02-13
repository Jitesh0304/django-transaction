from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



class BankAccount(models.Model):
    accountNumber = models.IntegerField(validators = [MinValueValidator(1001261015), MaxValueValidator(9701132007)], unique=True,
                                        blank=True)
    accountHolder = models.ForeignKey(User, on_delete=models.PROTECT, related_name= 'account_owner', blank=True)
    balance = models.FloatField(default=0)
    accountType = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.accountNumber)



class TransactionModel(models.Model):
    senderUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'sender_transaction', blank=True)
    receiverUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'receiver_transaction', blank=True)
    senderaccountNum = models.IntegerField(blank=False)
    receiveraccountNum = models.IntegerField(blank=False)
    amount = models.FloatField(blank=False)
    message = models.CharField(max_length=100, blank=True)