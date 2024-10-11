from django.contrib import messages
from django.shortcuts import render, redirect
from app.services.product_service import ProductService


def add_product(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, "Login first")
        return redirect('login')
    if user.role != "Auctioneer":
        messages.warning(request, "Access denied!")
        return redirect('home')
    if request.method == "POST":
        picture = request.FILES.get('picture')
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_price = request.POST.get("price")
        end_date = request.POST.get("date")
        end_time = request.POST.get("time")
        status, message, obj = ProductService().add_product(title, description, start_price, end_date, end_time, picture, user)
        if status:
            messages.success(request, message)
            return redirect('home')
        messages.warning(request, message)
        return redirect('add product')
    return render(request, 'seller/add_product.html')
