import random
import smtplib
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from myapp.models import account
from myapp.forms import accountForm, EmailForm, editForm, AccountNumberForm

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
                subject='Account Opening..!',
                message=f'Dear {user_info.fname} {user_info.lname},\n\nThank you for registering. We have received your information.\nYour Account No: {user_info.account_number}\n\nBest Regards,\nUNIQUE BANK',
                from_email='abhimangalur2@gmail.com',
                recipient_list=[user_info.email],
                fail_silently=False,
            )
            
            return redirect('home')
    else:
        form = accountForm()
    
    return render(request, 'user_form.html', {'form': form})

def delete_account(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        try:
            accounts = account.objects.get(account_number=account_number)
            accounts.delete()
            messages.success(request, 'Account successfully deleted.')
        except account.DoesNotExist:
            messages.error(request, 'No account found with this email.')
        
        return redirect('home')
    return render(request, 'delete_account.html')

def edit_accounts(request):
    return render(request, 'edit_accounts.html')

def edit_account(request):
    account_number = request.GET.get('account_number') if request.method == 'GET' else request.POST.get('account_number')
    
    # Fetch the account instance only once
    accounts = get_object_or_404(account, account_number=account_number)
    
    if request.method == 'POST':
        form = editForm(request.POST, request.FILES, instance=accounts)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'edit_account.html', {'form': form, 'error': 'Form is invalid', 'account_number': account_number})

    else:  # Handle GET request
        form = editForm(instance=accounts)
        return render(request, 'edit_account.html', {'form': form, 'account_number': account_number})

def check_account(request):
    if request.method == 'POST':
        form = AccountNumberForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data['account_number'].strip()  # Remove any extra spaces
            print(f"Checking for account number: '{account_number}'")  # Debugging output

            try:
                accounts = account.objects.get(account_number=account_number)
                print(f"Account found: {accounts}")  # Debugging output
            except account.DoesNotExist:
                print("Account not found")  # Debugging output
                return render(request, 'check_account.html', {'form': form, 'error': 'Account number does not exist'})

            # Check if the 12-digit number and 6-digit pin already exist
            if accounts.generated_number and accounts.pin:
                # If they already exist, show an error message
                return render(request, 'check_account.html', {
                    'form': form,
                    'error': 'ATM details already exist for this account.'
                })
            
            # Generate a 12-digit number and a 6-digit pin
            generated_number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
            pin = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Save the generated values in the account
            accounts.generated_number = generated_number
            accounts.pin = pin
            accounts.save()

            # Send an email with the generated number and pin
            send_mail(
                'Your Account Details',
                f'Here are your account details:\n\n12-digit number: {generated_number}\n6-digit pin: {pin}',
                'abhimangalur2@gmail.com',
                [accounts.email],
                fail_silently=False,
            )

            return redirect('home')  # Redirect to the homepage after processing

    else:
        form = AccountNumberForm()

    return render(request, 'check_account.html', {'form': form})
