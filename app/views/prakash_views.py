from django.shortcuts import render

def data_listing(request):
    return render(request,"model_checking/data_listing.html")

def win(request):
    return render(request,"seller/win.html")

def edit_profile(request):
    return render(request,"authentication/edit_profile.html")

def bidder_edit_profile(request):
    return render(request,"authentication/bidder_edit_profile.html")