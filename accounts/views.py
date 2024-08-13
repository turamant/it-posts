from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html',{'error': 'Пользователь с таким именем уже существует'})
            
        user = User(username=username, password=password)
        user.set_password(password)
        user.save()
        return redirect('accounts:login')
    return render(request, 'accounts/register.html')
    
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts:list')
        return render(request, 'accounts/login.html', {'error': 'Неправильный логин или пароль'})
    return render(request, 'accounts/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('posts:list')
         
