from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction, Account, Category

class SignUpForm(UserCreationForm):
    class Meta: model = User; fields = ("username","password1","password2")

class TransactionForm(forms.ModelForm):
    class Meta: model = Transaction; fields = ("account","category","kind","amount","date","description")
    def __init__(self,*a,**k):
        user = k.pop("user")
        super().__init__(*a,**k)
        self.fields["account"].queryset = Account.objects.filter(owner=user)
        self.fields["category"].queryset = Category.objects.filter(owner=user)

class AccountForm(forms.ModelForm):
    class Meta: model = Account; fields = ("name",)

class CategoryForm(forms.ModelForm):
    class Meta: model = Category; fields = ("name",)
