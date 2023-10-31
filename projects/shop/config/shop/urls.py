from django.urls import path

from .views import *

urlpatterns = [
    path('', catalog, name='catalog'),
    path('orders/', orders, name='orders'),
    path('order_create/', order_create, name='order_create'),
    path('product/<int:id>/', product_detail, name='product_detail'),
]
