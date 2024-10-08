from django.shortcuts import render

def data_listing(request):
    return render(request,"model_checking/data_listing.html")

def win(request):
    return render(request,"seller/win.html")