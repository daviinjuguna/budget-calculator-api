from django.urls import path
from knox import views as knox_views

from .views import *

urlpatterns = [
    path('login/', LoginApi.as_view(), name="login"),
    path('register/', RegisterApi.as_view(), name='register'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('income/',IncomeApi.as_view(),name="income"),
    path('expense/',ExpenseApi.as_view(),name="expense"),
    path('profile/',UserAPI.as_view(), name="profile")
]
