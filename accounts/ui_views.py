from django.shortcuts import render

def landing_view(request):
    return render(request, 'landing.html')

def login_view(request):
    return render(request, 'auth/login.html')

def register_view(request):
    return render(request, 'auth/register.html')
