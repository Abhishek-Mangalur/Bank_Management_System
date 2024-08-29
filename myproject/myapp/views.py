from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import accountForm

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            return HttpResponse('Invalid login')
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def custom_logout(request):
    logout(request)
    return redirect('/login/')

def user_form(request):
    if request.method == 'POST':
        form = accountForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = accountForm()
    
    return render(request, 'user_form.html', {'form': form})

def user_form(request):
    if request.method == 'POST':
        form = accountForm(request.POST, request.FILES)
        if form.is_valid():
            user_info = form.save()
            
            # Send a confirmation email
            send_mail(
                subject='Thank You for Registering!',
                message=f'Dear {user_info.name},\n\nThank you for registering. We have received your information.\n\nBest Regards,\nUNIQUE BANK',
                from_email='abhimangalur2@gmail.com',
                recipient_list=[user_info.email],
                fail_silently=False,
            )
            
            return redirect('home')
    else:
        form = accountForm()
    
    return render(request, 'user_form.html', {'form': form})
