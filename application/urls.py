from django.urls import path
from .views import UserLoginView , BankAccountView, UserRegisterView, TransactionModelView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('bank/', BankAccountView.as_view(), name='bank'),
    path('trans/', TransactionModelView.as_view(), name='trans')
]
