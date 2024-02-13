from .models import BankAccount, TransactionModel
from .serializers import BankAccountSerializer, UserLoginSerializer, TransactionModelSerializer, UserRegisterSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from django.contrib.auth.models import User
import random
from django.db import transaction




def get_tokens_for_user(user):
    refreshToken = RefreshToken.for_user(user)
    accessToken = refreshToken.access_token
            ## decode the JWT .... mension the same name of th e secrete_key what ever you have written in .env file
    decodeJTW = jwt.decode(str(accessToken), settings.SECRET_KEY, algorithms=["HS256"])
            # add payload here!!
    decodeJTW['user'] = str(user)
            # encode
    encoded = jwt.encode(decodeJTW, settings.SECRET_KEY, algorithm="HS256")
    return {
        'access': str(encoded),
        'refresh': str(refreshToken),
    }





class UserRegisterView(APIView):
    def post(self, request, format= None):
        serializer = UserRegisterSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Account created successfully.....'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST) 


class UserLoginView(APIView):
    def post(self, request, format= None):
        serializer = UserLoginSerializer(data= request.data)
        if serializer.is_valid():

                        ## If a user send some extra fields data.. Then this error will occure
            input_data = set(serializer.initial_data.keys())
            required_fields = set(serializer.fields.keys())
            ext_data =  input_data - required_fields
            if ext_data:
                return Response({'msg':f"You have provided extra field {ext_data}"}, status.HTTP_400_BAD_REQUEST)
            
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username= username, password = password)
            if user is not None:
                user = User.objects.get(username= username)
                token = get_tokens_for_user(user)
                return Response({'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'msg':'Email or Password is not Valid'},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST) 





class BankAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        try:
            serializer = BankAccountSerializer(data= request.data, context={'request':request})
            if serializer.is_valid():
                all_account = BankAccount.objects.all().values_list('accountNumber', flat=True)
                while True:
                    value = random.randint(1001261015, 9701132007)
                    if value not in all_account:
                        serializer.save(accountNumber= value)
                        break
                return Response({'account_data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)




# class BankAccountView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, format=None):
#         user = request.user
#         try:
#             serializer = BankAccountSerializer(data= request.data, context={'request':request})
#             if serializer.is_valid():
#                 all_account = BankAccount.objects.all().values_list('accountNumber', flat=True)
#                 all_account = [1,2,3,4]
#                 while True:
#                     # value = random.randint(1, 5)
#                     value = random.randint(1001261015, 9701132007)
#                     if value not in all_account:
#                         serializer.save(accountNumber= value)
#                         break
#                 # print(serializer.validated_data)
#                 return Response({'account_data': serializer.data}, status=status.HTTP_200_OK)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        




class TransactionModelView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, format=None):
        user = request.user
        try:
            serializer = TransactionModelSerializer(data= request.data, context={'request':request})
            if serializer.is_valid():
                # receiver = serializer.validated_data['receiverUser']
                # senderaccountNum = serializer.validated_data['senderaccountNum']
                # receiveraccountNum = serializer.validated_data['receiveraccountNum']
                # amount = serializer.validated_data['amount']
                # try:
                #     sender_bankdata = BankAccount.objects.get(accountHolder= user, accountNumber=senderaccountNum)
                # except Exception:
                #     return Response({'msg':"This account does not belong to you...."}, status=status.HTTP_400_BAD_REQUEST)
                # try:
                #     receiver_bankdata = BankAccount.objects.get(accountHolder= receiver, accountNumber=receiveraccountNum)
                # except Exception:
                #     return Response({'msg':f'Account number does not belong to -{receiver.username}- receiver.....'}, 
                #                     status=status.HTTP_400_BAD_REQUEST)
                
                # if sender_bankdata.balance >= amount:
                #     sender_bankdata.balance = sender_bankdata.balance - amount

                #     receiver_bankdata.balance = receiver_bankdata.balance + amount
                #     sender_bankdata.save()
                #     receiver_bankdata.save()
                #     serializer.save()
                #     return Response({'msg':'Transaction successful .....'}, status=status.HTTP_200_OK)
                # else:
                #     return Response({'msg':"You don't not have sufficient balance ..."}, status=status.HTTP_400_BAD_REQUEST)

                                ###### OR ########

                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)