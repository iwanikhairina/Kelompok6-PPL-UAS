from django.urls import path
from . import admin_views

app_name = 'admin'

urlpatterns = [
    # Dashboard
    path('', admin_views.admin_dashboard, name='dashboard'),
    
    # Voucher URLs
    path('vouchers/', admin_views.voucher_list, name='voucher_list'),
    path('vouchers/create/', admin_views.voucher_create, name='voucher_create'),
    path('vouchers/<int:pk>/edit/', admin_views.voucher_edit, name='voucher_edit'),
    path('vouchers/<int:pk>/delete/', admin_views.voucher_delete, name='voucher_delete'),
    
    # Category URLs
    path('categories/', admin_views.category_list, name='category_list'),
    path('categories/create/', admin_views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', admin_views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', admin_views.category_delete, name='category_delete'),
]