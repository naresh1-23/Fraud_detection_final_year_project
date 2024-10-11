from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from app.services.user_service import UserService


def user_login(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get("password")
        status, message, obj = UserService().login_user(email, password)
        print(message)
        if status:
            login(request, obj)
            messages.success(request, message)
            return redirect('home')
        messages.warning(request, message)
        return redirect('login')
    return render(request, 'authentication/login.html')


def register(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get('role')
        status, message, obj = UserService().register_user(email, password, confirm_password, role)
        print(message)
        if status:
            messages.success(request, message)
            return redirect('login')
        messages.warning(request, message)
        return redirect('register')
    return render(request, 'authentication/register.html')
