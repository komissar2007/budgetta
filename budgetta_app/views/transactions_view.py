import datetime

from django.contrib.auth.decorators import login_required
from budgetta_app.forms import TransactionForm
from budgetta_app.models import Transaction, Category
from budgetta_app.utils import shared_utils
from django.shortcuts import render, redirect


@login_required
def transactions(request):
    """show all transactions"""
    today = datetime.datetime.now()
    transactions_query_set = Transaction.objects.filter(owner=request.user, date__year=today.year,
                                              date__month=today.month).order_by('-date')
    categories = Category.objects.filter(owner=request.user)
    expenses = []
    incomes = []
    for transaction in transactions_query_set:
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


def edit_transaction_modal(request):
    """edit transaction from modal"""
    transaction_id = request.POST['transaction']
    transaction = Transaction.objects.get(owner=request.user, id=transaction_id)
    if request.POST['edit'] == 'delete':
        transaction.delete()
        return redirect('budgetta_app:transactions')
    if request.POST['edit'] == 'submit':
        form = TransactionForm(instance=transaction, data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('budgetta_app:transactions')
    return redirect('budgetta_app:transactions')
