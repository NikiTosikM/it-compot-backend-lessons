from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def signup(request):
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
    return render(request, 'Core/auth/signin.html')
