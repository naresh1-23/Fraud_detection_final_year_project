from django.contrib import messages
from django.shortcuts import render, redirect
from app.models import UserStatistics
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
            ProductService().update_user_stats_item_listed(user)
            messages.success(request, message)
            return redirect('home')
        messages.warning(request, message)
        return redirect('add product')
    return render(request, 'seller/add_product.html')


def your_product(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, "Login first")
        return redirect('login')
    if user.role != "Auctioneer":
        messages.warning(request, "Access denied!")
        return redirect('home')
    products = ProductService().filter_product(seller=user)
    return render(request, "product/your_product.html", {"products": products})


def sold_product(request, product_id):
    user = request.user
    product = ProductService().get_product(id=product_id)
    user_stats = UserStatistics.objects.filter(user=user).first()
    user_stats.total_item_sold += 1
    user_stats.save()
    product.is_sold = True
    product.save()
    messages.success(request, "Sold Item")
    return redirect('your product')
