from django.shortcuts import render


def add_product(request):
    return render(request, 'seller/add_product.html')
