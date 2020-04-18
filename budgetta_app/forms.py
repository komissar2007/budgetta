from django import forms

from .models import Transaction, Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['name', 'amount', 'is_expense', 'category']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(owner=self.user)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'limit', 'is_expense']
