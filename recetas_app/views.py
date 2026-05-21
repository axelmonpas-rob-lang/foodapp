from django.shortcuts import render

def home(request):
    return render(request, 'store/home.html')

def login_view(request):
    return render(request, 'store/login.html')

def register_view(request):
    return render(request, 'store/register.html')