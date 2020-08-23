from budgetta_app.utils import shared_utils
from django.shortcuts import render


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
