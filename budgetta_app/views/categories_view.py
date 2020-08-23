from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your views here.
from django.shortcuts import render, redirect
from budgetta_app.forms import CategoryForm
from budgetta_app.models import Category
from budgetta_app.utils import shared_utils


@login_required
def categories(request):
    """show all categories"""
    categories = Category.objects.filter(owner=request.user).order_by('date')
    expense_sum = 0
    income_sum = 0
    for category in categories:
        if category.is_expense:
            expense_sum += category.limit
        else:
            income_sum += category.limit
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
            category = form.save(commit=False)
            category.owner = request.user
            category.save()
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
