from rest_framework import serializers
from .models import BankAccount, TransactionModel
from django.contrib.auth.models import User
from django.db import transaction



class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 255)
    password = serializers.CharField(max_length = 255)
    # class Meta:
    #     model = User
    #     fields = ['username','password']



class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = "__all__"


    def create(self, validated_data): 
        ## take thhe user details from the context of view class
        user = self.context['request'].user
        ## save the accountHolder name in annotatedBy field
        validated_data['accountHolder'] = user
        return super().create(validated_data)




class TransactionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = "__all__"

    def create(self, validated_data): 
        ## take thhe user details from the context of view class
        user = self.context['request'].user
        ## save the senderUser name in annotatedBy field
        validated_data['senderUser'] = user
        return super().create(validated_data)

    def validate(self, data):
        with transaction.atomic():
            senderUser = self.context['request'].user
            receiver = data.get('receiverUser')
            senderaccountNum = data.get('senderaccountNum')
            receiveraccountNum = data.get('receiveraccountNum')
            amount = data.get('amount')
            try:
                sender_bankdata = BankAccount.objects.get(accountHolder= senderUser, accountNumber=senderaccountNum)
            except Exception:
                raise serializers.ValidationError("This account does not belong to you....")
            try:
                receiver_bankdata = BankAccount.objects.get(accountHolder= receiver, accountNumber=receiveraccountNum)
            except Exception:
                raise serializers.ValidationError(f'Account number does not belong to -{receiver.username}- receiver.....')
            
            if sender_bankdata.balance >= amount:
                sender_bankdata.balance = sender_bankdata.balance - amount

                receiver_bankdata.balance = receiver_bankdata.balance + amount
                sender_bankdata.save()
                receiver_bankdata.save()
            return data