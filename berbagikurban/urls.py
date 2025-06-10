# berbagikurban/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.splashscreen, name='splash'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_view, name='home'),
    path('voucher/<int:voucher_id>/', views.voucher_detail, name='voucher_detail'),
    path('klaim/<int:voucher_id>/', views.klaim_voucher, name='klaim_voucher'),
    path('success/<int:voucher_id>/', views.voucher_success, name='voucher_success'),  # Route yang hilang
    path('logout/', views.logout_view, name='logout'),
]