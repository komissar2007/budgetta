from django import forms

from .models import Transaction, Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'amount', 'is_expense', 'category']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'limit', 'is_expense']


