from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from app.models import Bidding, BiddingWinner
from app.services.product_service import ProductService


def home(request):
    if request.method == "POST":
        search = request.POST.get('search', "")
        products = ProductService().filter_product(bidding_ending_date__gte=datetime.now(), name__icontains=search)
    else:
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


def bidder_bids(request):
    user = request.user
    bids = Bidding.objects.filter(bidder=user)
    total_bids = []
    if bids:
        for bid in bids:
            temp = {}
            if bid.product.bidding_ending_date > datetime.now().date():
                status = "Pending"
            elif bid.product.bidding_ending_date == datetime.now().date():
                if bid.product.bidding_ending_time < datetime.now().time():
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
    print(bids)
    print(total_bids[0]["bid"])
    return render(request, "product/bidder_bids.html", {"bids": total_bids})


def bids_won(request):
    user = request.user
    bids = BiddingWinner.objects.filter(bidding__bidder=user)
    return render(request, "product/bids_won.html", {"bids": bids})
