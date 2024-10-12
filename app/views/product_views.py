from datetime import datetime
from django.shortcuts import render
from app.services.product_service import ProductService


def home(request):
    products = ProductService().filter_product(bidding_ending_date__gte=datetime.now())
    data = {
        "products": products
    }
    print(products[0].picture)
    return render(request, 'product/home.html', data)


def bid(request, pk):
    product = ProductService().get_product(id=pk)
    data = {
        "product": product
    }
    return render(request, 'product/bid.html', data)
