from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-money/', views.add_money, name='add money'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]
