from django.shortcuts import render


def signup(request):
    return render(request, 'Core/auth/signup.html')


def signin(request):
    return render(request, 'Core/auth/signin.html')
