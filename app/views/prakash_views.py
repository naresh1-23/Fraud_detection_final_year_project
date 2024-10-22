from django.shortcuts import render


def win(request):
    return render(request, "seller/win.html")


def edit_profile(request):
    return render(request, "authentication/edit_profile.html")


def bidder_edit_profile(request):
    return render(request, "authentication/bidder_edit_profile.html")


def your_product(request):
    return render(request, "product/your_product.html")


def bidder_bids(request):
    return render(request, "product/bidder_bids.html")


def bids_won(request):
    return render(request, "product/bids_won.html")
