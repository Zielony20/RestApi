from django.urls import path
from . import views

urlpatterns = [

    path('api/years', views.getYears, name="list"),
    path('api/years/<int:pk_year>',views.getYear),
    path('api/users',views.getUsers),
    path('api/users/<int:pk_u>',views.getUser),
    path('api/years/<int:pk_year>/members',views.getMembers),
    path('api/years/<int:pk_year>/members/<int:pk_mem>/contributions',views.getContributions),
    path('api/years/<int:pk_year>/members/<int:pk_mem>/contributions/<int:pk_con>',views.getContribution),
    path('api/years/<int:pk_year>/incomes',views.getIncomes),
    path('api/years/<int:pk_year>/incomes/<int:pk_inc>',views.getIncome),
    path('api/years/<int:pk_year>/expenditures',views.getExpenditures),
    path('api/years/<int:pk_year>/expenditures/<int:pk_exp>',views.getExpenditure),
    path('api/budget',views.getBudget),
    path('api/budget/<int:pk_year>',views.getBudgetYear),



    #path('list', views.ApiYearListView.as_view(), name="list"),
    
    #path('years/', views.getYears),
    #path('api/years/add', views.addYear),
    #path('api/years/<str:pk_year>/update',views.updateYear),
    #path('api/years/<str:pk_year>/delete',views.deleteYear),

    #path('api/users/add',views.addUser),
    #path('api/users/<int:pk_u>/delete',views.deleteUser),
    #path('api/users/<int:pk_u>/update',views.updateUser),
    #path('api/users/<int:pk_u>/patch',views.patchUser),
    
    
    #path('api/years/<int:pk_year>/members/<int:pk_mem>/contributions/add',views.addContributions),
    #path('api/years/<int:pk_year>/members/<int:pk_mem>/contributions/<int:pk_con>/delete',views.deleteContributions),
    #path('api/years/<int:pk_year>/members/<int:pk_mem>/contributions/<int:pk_con>/update',views.updateContributions),

    #path('api/years/<int:pk_year>/incomes/add',views.addIncome),    
    #path('api/years/<int:pk_year>/incomes/<int:pk_inc>/update',views.updateIncome),
    #path('api/years/<int:pk_year>/incomes/<int:pk_inc>/delete',views.deleteIncome),

    #path('api/years/<int:pk_year>/expenditures/add',views.addExpenditure),
    #path('api/years/<int:pk_year>/expenditures/<int:pk_exp>/update',views.updateExpenditure),
    #path('api/years/<int:pk_year>/expenditures/<int:pk_exp>/delete',views.deleteExpenditure),
    #path('api/years/<int:pk_year>/expenditures/<int:pk_exp>/patch',views.patchExpenditure),
 

    path('api/years/<int:pk_year>/members/<int:pk_mem>',views.getMember),
    path('api/years/<int:pk_year>/members/<int:pk_mem>',views.getMember),


]




