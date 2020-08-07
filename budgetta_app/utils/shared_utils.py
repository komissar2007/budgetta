import datetime

from budgetta_app.models import Transaction, Category
from django.db.models import Sum


def get_category_by_sum(user):
    today = datetime.datetime.now()
    amount =  Transaction.objects.values('category', 'category__name', 'is_expense',
                                      'category__limit').filter(owner=user,
                                                                date__year=today.year,
                                                                date__month=today.month).annotate(
        total_price=Sum('amount'))
    if (amount == 0):
        return 1
    else:
        return amount

def get_total_expenses(user):
    today = datetime.datetime.now()
    amount = Transaction.objects.values('category', 'category__name', 'is_expense',
                                      'category__limit').filter(owner=user,
                                                                date__year=today.year,
                                                                is_expense=True,
                                                                date__month=today.month).aggregate(
        sum=Sum('amount'))

    if (amount['sum'] is None):
        amount['sum'] = 1
        return amount
    else:
        return amount

def get_expected_expenses(user):
    amount =  Category.objects.filter(owner=user, is_expense=True).aggregate(sum=Sum('limit'))
    if (amount['sum'] is None):
        amount['sum'] = 1
        return amount
    else:
        return amount