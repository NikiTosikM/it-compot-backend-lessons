from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def profile(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'Core/auth/profile.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        r_password = request.POST['repeat_password']
        if password != r_password:
            return render(request, 'Core/auth/signup.html', {
                'error': 'Пароли не совпадают.'
            })
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return redirect('signin')
    return render(request, 'Core/auth/signup.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request, username=username, password=password
        )
        if user is not None:
            login(request, user)
            return redirect('catalog')
        else:
            return render(request, 'Core/auth/signup.html', {
                'error': 'Неверный логин или пароль.'
            })
    return render(request, 'Core/auth/signin.html')


def signout(request):
    logout(request)
    return redirect('signin')
