from django.contrib.auth import login, logout, update_session_auth_hash
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


def user_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('login')
    return redirect("login")


def profile(request):
    user = request.user
    if request.method == "POST":
        email = request.POST.get('email')
        confirm_email = request.POST.get('confirm_email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not email and not password:
            messages.error(request, "Either email or password is required")
            return redirect('profile')
        if email:
            if email != confirm_email:
                messages.error(request, "Email didn't matched")
                return redirect('profile')
            another_user = UserService().get_user(email=email)
            if another_user:
                messages.error(request, "Email already exists")
                return redirect('profile')
            user.email = email
        if password:
            if password != confirm_password:
                messages.error(request, "Password didn't matched")
                return redirect('profile')
            user.set_password(password)  # Use set_password method
            update_session_auth_hash(request, user)
        user.save()
        messages.success(request, "Profile successfully edited")
        return redirect('profile')
    return render(request, 'authentication/edit_profile.html', {"user": user})
