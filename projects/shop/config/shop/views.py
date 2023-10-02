from django.shortcuts import render
from .models import Product, Order


def catalog(request):
    all_products = Product.objects.all()
    return render(request, 'shop/catalog.html', {'products': all_products})


def orders(request):
    orders_ = Order.objects.all()
    return render(request, 'shop/orders.html', {'orders': orders_})


def order_create(request):
    return render(request, 'shop/order_create.html')
