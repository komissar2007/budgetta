import datetime

from budgetta_app.models import Transaction, Category
from django.db.models import Sum


def get_category_by_sum(user):
    today = datetime.datetime.now()
    return Transaction.objects.values('category', 'category__name', 'is_expense',
                                      'category__limit').filter(owner=user,
                                                                date__year=today.year,
                                                                date__month=today.month).annotate(
        total_price=Sum('amount'))

def get_total_expenses(user):
    today = datetime.datetime.now()
    return Transaction.objects.values('category', 'category__name', 'is_expense',
                                      'category__limit').filter(owner=user,
                                                                date__year=today.year,
                                                                is_expense=True,
                                                                date__month=today.month).aggregate(
        sum=Sum('amount'))

def get_expected_expenses(user):
    return Category.objects.filter(owner=user, is_expense=True).aggregate(sum=Sum('limit'))