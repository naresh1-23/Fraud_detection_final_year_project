from django.shortcuts import render


def home(request):
    return render(request, 'product/home.html')


def bid(request):
    return render(request, 'product/bid.html')
