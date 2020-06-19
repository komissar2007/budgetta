import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from budgetta_app.forms import TransactionForm, CategoryForm
from budgetta_app.models import Transaction, Category


def index(request):
    today = datetime.datetime.now()
    if request.user.is_authenticated:
        category_by_sum = Transaction.objects.values('category', 'category__name', 'is_expense',
                                                     'category__limit').filter(owner=request.user,
                                                                               date__year=today.year,
                                                                               date__month=today.month).annotate(
            total_price=Sum('amount'))
        expense_list = []

        income_list = []

        for category in category_by_sum:
            if category['is_expense']:
                expense_list.append(category)
            else:
                income_list.append(category)

        context = {'expense_list': expense_list, 'income_list': income_list}
    else:
        context = {}

    return render(request, 'budgetta_app/index.html', context)


@login_required
def transactions(request):
    """show all transactions"""
    today = datetime.datetime.now()
    transactions = Transaction.objects.filter(owner=request.user, date__year=today.year,
                                              date__month=today.month).order_by('-date')
    categories = Category.objects.filter(owner=request.user)
    expenses = []
    incomes = []
    for transaction in transactions:
        transaction.date = transaction.date.strftime("%d-%m-%Y")
        if transaction.is_expense:
            expenses.append(transaction)
        else:
            incomes.append(transaction)

    context = {'expenses': expenses, 'incomes': incomes, 'categories': categories}
    return render(request, 'budgetta_app/transactions.html', context)


@login_required
def new_transaction(request):
    """add new transaction"""
    if request.method != 'POST':
        form = TransactionForm(user=request.user)
    else:
        form = TransactionForm(user=request.user, data=request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.owner = request.user
            transaction.save()
            return redirect('budgetta_app:transactions')
    context = {'form': form}
    return render(request, 'budgetta_app/new_transaction.html', context)




@login_required
def categories(request):
    """show all categories"""
    categories = Category.objects.filter(owner=request.user).order_by('date')
    expense_sum = 0
    income_sum = 0
    for category in categories:
        if (category.is_expense):
            expense_sum+=category.limit
        else:
            income_sum+=category.limit
    context = {'categories': categories, 'expense_sum': expense_sum, 'income_sum': income_sum}
    return render(request, 'budgetta_app/categories.html', context)


@login_required
def new_category(request):
    """add new category"""
    if request.method != 'POST':
        form = CategoryForm()
    else:
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.owner = request.user
            new_category.save()
            return redirect('budgetta_app:categories')
    context = {'form': form}
    return render(request, 'budgetta_app/new_category.html', context)


@login_required
def edit_category(request, category_id):
    """edit category"""
    category = Category.objects.get(owner=request.user, id=category_id)
    if category.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = CategoryForm(instance=category)
    elif request.POST['edit'] == 'submit':
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('budgetta_app:categories')
    elif request.POST['edit'] == 'delete':
        category.delete()
        return redirect('budgetta_app:categories')
    context = {'category': category, 'form': form}
    return render(request, 'budgetta_app/edit_category.html', context)
