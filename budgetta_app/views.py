import datetime

from django.contrib.auth.decorators import login_required

from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from budgetta_app.forms import TransactionForm, CategoryForm
from budgetta_app.models import Transaction, Category
from budgetta_app.utils import shared_utils


def index(request):
    if request.user.is_authenticated:
        category_by_sum = shared_utils.get_category_by_sum(request.user)
        expense_list = []
        income_list = []
        total_expenses = shared_utils.get_total_expenses(request.user)
        expected_expenses = shared_utils.get_expected_expenses(request.user)

        for category in category_by_sum:
            if category['is_expense']:
                expense_list.append(category)
            else:
                income_list.append(category)

        context = {'expense_list': expense_list,
                   'income_list': income_list,
                   'total_expenses': total_expenses,
                   'expected_expenses': expected_expenses}
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

    total_expenses = shared_utils.get_total_expenses(request.user)
    expected_expenses = shared_utils.get_expected_expenses(request.user)

    context = {'expenses': expenses, 'incomes': incomes, 'categories': categories,
               'total_expenses': total_expenses,
               'expected_expenses': expected_expenses}
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
    total_expenses = shared_utils.get_total_expenses(request.user)
    expected_expenses = shared_utils.get_expected_expenses(request.user)
    context = {'form': form,
               'total_expenses': total_expenses,
               'expected_expenses': expected_expenses}
    return render(request, 'budgetta_app/new_transaction.html', context)

def edit_transaction(request, transaction_id):
    """edit transaction"""
    transaction = Transaction.objects.get(owner=request.user, id=transaction_id)
    if request.method != 'POST':
        form = TransactionForm(instance=transaction, user=request.user)
    elif request.POST['edit'] == 'submit':
        form = TransactionForm(instance=transaction, data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('budgetta_app:transactions')
    elif request.POST['edit'] == 'delete':
        transaction.delete()
        return redirect('budgetta_app:transactions')
    total_expenses = shared_utils.get_total_expenses(request.user)
    expected_expenses = shared_utils.get_expected_expenses(request.user)
    context = {'transaction': transaction, 'form': form,
               'total_expenses': total_expenses,
               'expected_expenses': expected_expenses}
    return render(request, 'budgetta_app/edit_transaction.html', context)





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
    total_expenses = shared_utils.get_total_expenses(request.user)
    expected_expenses = shared_utils.get_expected_expenses(request.user)
    context = {'categories': categories, 'expense_sum': expense_sum, 'income_sum': income_sum,
               'total_expenses': total_expenses,
               'expected_expenses': expected_expenses}
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
    total_expenses = shared_utils.get_total_expenses(request.user)
    expected_expenses = shared_utils.get_expected_expenses(request.user)
    context = {'form': form,
               'total_expenses': total_expenses,
               'expected_expenses': expected_expenses}
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
    total_expenses = shared_utils.get_total_expenses(request.user)
    expected_expenses = shared_utils.get_expected_expenses(request.user)
    context = {'category': category, 'form': form,
               'total_expenses': total_expenses,
               'expected_expenses': expected_expenses}
    return render(request, 'budgetta_app/edit_category.html', context)
