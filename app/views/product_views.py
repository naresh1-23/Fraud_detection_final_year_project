from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
import pytz
from app.apps import AppConfig
from app.models import Bidding, BiddingWinner, UserStatistics
from app.services.product_service import ProductService


def home(request):
    if request.user.is_authenticated:
        ProductService().assign_winner()
        time_zone = pytz.timezone("Asia/Kathmandu")
        if request.method == "POST":
            search = request.POST.get('search', "")
            products = ProductService().filter_product(
                bidding_ending_date__gte=datetime.now(time_zone),
                name__icontains=search).exclude(
                bidding_ending_date=datetime.now(time_zone).date(),
                bidding_ending_time__lte=datetime.now(time_zone).time())
        else:
            products = ProductService().filter_product(
                bidding_ending_date__gte=datetime.now(time_zone)).exclude(
                bidding_ending_date=datetime.now(time_zone).date(),
                bidding_ending_time__lte=datetime.now(time_zone).time())
        new_products = []
        for product in products:
            temp = {}
            temp["product"] = product
            user = product.seller
            temp["fraud"] = ProductService().predict_fraud(user)
            new_products.append(temp)
        data = {
            "products": new_products
        }

        return render(request, 'product/home.html', data)
    return redirect('login')


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


def bidder_bids(request):
    user = request.user
    time_zone = pytz.timezone("Asia/Kathmandu")
    bids = Bidding.objects.filter(bidder=user)
    total_bids = []
    if bids:
        for bid in bids:
            temp = {}
            if bid.product.bidding_ending_date > datetime.now(time_zone).date():
                status = "Pending"
            elif bid.product.bidding_ending_date == datetime.now(time_zone).date():
                if bid.product.bidding_ending_time < datetime.now(time_zone).time():
                    result = BiddingWinner.objects.filter(bidding=bid).first()
                    if result:
                        status = "Won"
                    else:
                        status = "Loss"
                else:
                    status = "Pending"
            else:
                result = BiddingWinner.objects.filter(bidding=bid).first()
                if result:
                    status = "Won"
                else:
                    status = "Loss"

            temp["bid"] = bid
            temp["status"] = status
            total_bids.append(temp)
    return render(request, "product/bidder_bids.html", {"bids": total_bids})


def bids_won(request):
    user = request.user
    bids = BiddingWinner.objects.filter(bidding__bidder=user)
    return render(request, "product/bids_won.html", {"bids": bids})
