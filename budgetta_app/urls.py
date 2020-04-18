from django.urls import path, include

from budgetta_app import views

app_name = 'budgetta_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('transactions/', views.transactions, name='transactions'),
    path('new_transaction/', views.new_transaction, name='new_transaction'),
    path('categories/', views.categories, name='categories'),
    path('new_categroy/', views.new_category, name='new_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
]
