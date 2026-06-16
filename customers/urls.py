from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
     path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_customer, name='add_customer'),
    path('update/<int:pk>/', views.update_payment, name='update_payment'),
    path('delete/<int:pk>/', views.delete_customer, name='delete_customer'),
    path(
    'customer/<int:pk>/',
    views.customer_detail,
    name='customer_detail'
),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path(
    'customer/<int:pk>/add-service/',
    views.add_service,
    name='add_service'
),
path(
    'download-pdf/',
    views.download_pdf,
    name='download_pdf'
),
path(
    'expense-report/',
    views.expense_report_pdf,
    name='expense_report_pdf'
),
path(
    'expenses/',
    views.expense_list,
    name='expense_list'
),

path(
    'expenses/add/',
    views.add_expense,
    name='add_expense'
),
]