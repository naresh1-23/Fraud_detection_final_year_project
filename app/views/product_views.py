from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from app.models import Bidding
from app.services.product_service import ProductService


def home(request):
    products = ProductService().filter_product(bidding_ending_date__gte=datetime.now())
    data = {
        "products": products
    }
    return render(request, 'product/home.html', data)


def bid(request, pk):
    product = ProductService().get_product(id=pk)
    data = {
        "product": product
    }
    if request.method == "POST":
        price = request.POST.get('bid_price')
        if int(price) < int(product.starting_price):
            messages.warning(request, "Invalid Price")
            return render(request, 'product/bid.html', data)
        product.starting_price = price
        product.save()
        bid = Bidding.objects.create(price=int(price), bidder=request.user, product=product)
        bid.save()
        messages.success(request, "Successfully bid added")
        return render(request, 'product/bid.html', data)
    return render(request, 'product/bid.html', data)
