from django.contrib import admin
from .models import BankAccount, TransactionModel

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("id","accountNumber", "accountHolder","balance","accountType","branch")

@admin.register(TransactionModel)
class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ("id","senderUser", "receiverUser","senderaccountNum","receiveraccountNum","amount", "message")