"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp.views import custom_login, home, custom_logout, user_form, delete_account, edit_account, edit_accounts, check_account, deposite_amount, withdraw_amount, atm_redirect, atm_options, balance_enquiry, deposit, withdraw

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', custom_login, name='login'),
    path('login/', custom_login, name='login'),
    path('home/', home, name='home'),
    path('logout/', custom_logout, name='login'),
    path('form/', user_form, name='user_form'),
    path('delete/', delete_account, name='delete_account'),
    path('edit/', edit_account, name='edit_account'),
    path('edits/', edit_accounts, name='edit_accounts'),
    path('account/', check_account, name='check_account'),
    path('deposite/', deposite_amount, name='deposite_amount'),
    path('withdraw/', withdraw_amount, name='withdraw_amount'),

    # path('withdraw/', withdraw_amount, name='withdraw_amount'),
    path('atm/', atm_redirect, name='atm_redirect'),
    path('atm/options/<str:generated_number>/', atm_options, name='atm_options'),
    path('balance/<str:generated_number>/', balance_enquiry, name='balance_enquiry'),
    path('atmdeposit/<str:generated_number>/', deposit, name='deposit'),
    path('atmwithdraw/<str:generated_number>/', withdraw, name='withdraw'),
]