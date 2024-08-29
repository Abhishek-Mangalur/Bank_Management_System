from django.urls import path
from .views import custom_login, home, custom_logout

urlpatterns = [
    path('login/', custom_login, name='login'),
    path('home/', home, name='home'),
    path('logout/', custom_logout, name='logout'),
]
