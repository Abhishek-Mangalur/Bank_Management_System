import random
import smtplib
# from django.db import transaction
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from myapp.models import account, transactions
from myapp.forms import accountForm, EmailForm, editForm, AccountNumberForm, DepositeForm, UpdateAmountForm, NumberForm, PinForm, AtmDepositForm


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
            # Retrieve the account using the account number
            accounts = account.objects.get(account_number=account_number)
            registered_email = accounts.email  # Assuming the 'account' model has an 'email' field
            # Delete the account
            accounts.delete()
            # Send a success message to the user's email
            send_mail(
                'Account Deletion Confirmation',
                'Your account has been successfully deleted.\nThank You for Using UNIQUE BANK Services\n\nBest Regards,\nUNIQUE BANK',
                'abhimangalur2@gmail.com',  # Replace with your "from" email
                [registered_email],
                fail_silently=False,
            )
            messages.success(request, 'Account successfully deleted. A confirmation email has been sent.')
        except account.DoesNotExist:
            messages.error(request, 'No account found with this account number.')
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

def atmappln(request):
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
                'Your ATM Details',
                f'Here are your ATM Card details:\n\n12-digit number: {generated_number}\n6-digit pin: {pin}',
                'abhimangalur2@gmail.com',
                [accounts.email],
                fail_silently=False,
            )
            return redirect('home')  # Redirect to the homepage after processing
    else:
        form = AccountNumberForm()
    return render(request, 'check_account.html', {'form': form})

def deposite_amount(request):
    account_details = None
    error = None
    form = DepositeForm(request.POST or None)
    update_form = UpdateAmountForm(request.POST or None)

    if request.method == 'POST':
        if 'fetch_details' in request.POST:
            if form.is_valid():
                account_number = form.cleaned_data['account_number'].strip()
                try:
                    account_details = account.objects.get(account_number=account_number)
                except account.DoesNotExist:
                    error = 'Account number does not exist'
        
        elif 'update_amount' in request.POST:
            if update_form.is_valid():
                account_number = update_form.cleaned_data['account_number'].strip()
                new_amount = update_form.cleaned_data['new_amount']

                try:
                    with transaction.atomic():
                        accounts = account.objects.get(account_number=account_number)
                        accounts.amount += new_amount
                        accounts.save()

                        # Save the transaction with account_number
                        transactions.objects.create(
                            account_number=account_number,
                            transaction_type='D',  # 'D' for Deposit
                            amount=new_amount,
                            total_amount=accounts.amount,
                            description='Deposit via BANK'
                        )
                    return redirect('home')
                except account.DoesNotExist:
                    error = 'Account number does not exist'
    
    else:
        if account_details:
            update_form = UpdateAmountForm(initial={'account_number': account_details.account_number})

    return render(request, 'deposit_amount.html', {
        'form': form,
        'update_form': update_form,
        'account_details': account_details,
        'error': error
    })

def withdraw_amount(request):
    account_details = None
    error = None
    form = DepositeForm(request.POST or None)
    update_form = UpdateAmountForm(request.POST or None)

    if request.method == 'POST':
        if 'fetch_details' in request.POST:
            if form.is_valid():
                account_number = form.cleaned_data['account_number'].strip()
                try:
                    account_details = account.objects.get(account_number=account_number)
                except account.DoesNotExist:
                    error = 'Account number does not exist'
        
        elif 'update_amount' in request.POST:
            if update_form.is_valid():
                account_number = update_form.cleaned_data['account_number'].strip()
                new_amount = update_form.cleaned_data['new_amount']

                try:
                    accounts = account.objects.get(account_number=account_number)
                    
                    if new_amount <= accounts.amount:  # Check if withdrawal amount is less than or equal to the existing amount
                        with transaction.atomic():
                            # Update the account balance
                            accounts.amount -= new_amount
                            accounts.save()

                            # Save the transaction with the updated total_amount
                            transactions.objects.create(
                                account_number=account_number,
                                transaction_type='W',  # 'W' for Withdraw
                                amount=new_amount,
                                total_amount=accounts.amount,  # Store the updated balance
                                description='Withdraw via BANK'
                            )
                        return redirect('home')
                    else:
                        error = 'Insufficient funds. Please enter a smaller amount.'
                except account.DoesNotExist:
                    error = 'Account number does not exist'
    
    else:
        if account_details:
            update_form = UpdateAmountForm(initial={'account_number': account_details.account_number})

    return render(request, 'withdraw_amount.html', {
        'form': form,
        'update_form': update_form,
        'account_details': account_details,
        'error': error
    })

def atm_redirect(request):
    error = None
    number_form = NumberForm(request.POST or None)

    if request.method == 'POST':
        if number_form.is_valid():
            generated_number = number_form.cleaned_data.get('generated_number').strip()
            try:
                account_details = account.objects.get(generated_number=generated_number)
                # If account exists, redirect to the options page with the generated number
                return redirect('atm_options', generated_number=generated_number)
            except account.DoesNotExist:
                error = 'Invalid ATM card number'

    return render(request, 'atm_redirect.html', {
        'number_form': number_form,
        'error': error
    })


def atm_options(request, generated_number):
    try:
        account_details = account.objects.get(generated_number=generated_number)
    except account.DoesNotExist:
        return redirect('atm_redirect')

    return render(request, 'atm_options.html', {
        'generated_number': generated_number,
        'account_details': account_details
    })


def balance_enquiry(request, generated_number):
    try:
        account_details = account.objects.get(generated_number=generated_number)
        balance = account_details.amount
    except account.DoesNotExist:
        return redirect('atm_redirect')

    return render(request, 'balance_enquiry.html', {
        'balance': balance,
        'generated_number': generated_number,
    })

def deposit(request, generated_number):
    account_details = None
    pin_error = None
    pin_validated = False  # To check if the PIN was validated
    form = PinForm(request.POST or None)
    deposit_form = None

    try:
        account_details = account.objects.get(generated_number=generated_number)
    except account.DoesNotExist:
        return redirect('atm_redirect')  # Handle non-existing account

    if request.method == 'POST':
        if 'check_pin' in request.POST and form.is_valid():
            entered_pin = form.cleaned_data.get('pin')
            if entered_pin == account_details.pin:
                pin_validated = True  # PIN is validated, show deposit form
                deposit_form = AtmDepositForm()  # Initialize the deposit form without POST data
            else:
                pin_error = 'Incorrect PIN. Please try again.'

        elif 'submit_deposit' in request.POST:
            deposit_form = AtmDepositForm(request.POST)
            if deposit_form.is_valid():
                new_amount = deposit_form.cleaned_data.get('amount')
                if new_amount > 0:
                    with transaction.atomic():
                        # Update the account balance
                        account_details.amount += new_amount
                        account_details.save()

                        # Save the transaction
                        transactions.objects.create(
                            account_number=account_details.account_number,
                            transaction_type='D',  # 'D' for Deposit
                            amount=new_amount,
                            total_amount=account_details.amount,  # Store the updated balance
                            description='Deposit via ATM'
                        )

                    # Redirect to the ATM options page after a successful deposit
                    return redirect('atm_options', generated_number=generated_number)
                else:
                    pin_error = 'Amount must be positive.'
            else:
                pin_validated = True  # Ensure the deposit form is displayed again

    # Render the form if the PIN was validated
    if pin_validated and deposit_form is None:
        deposit_form = AtmDepositForm()

    return render(request, 'deposit.html', {
        'form': form,
        'deposit_form': deposit_form,
        'pin_error': pin_error,
        'pin_validated': pin_validated,
        'generated_number': generated_number,
    })

def withdraw(request, generated_number):
    account_details = None
    pin_error = None
    pin_validated = False  # To check if the PIN was validated
    form = PinForm(request.POST or None)
    deposit_form = None

    try:
        account_details = account.objects.get(generated_number=generated_number)
    except account.DoesNotExist:
        return redirect('atm_redirect')  # Handle non-existing account

    if request.method == 'POST':
        if 'check_pin' in request.POST and form.is_valid():
            entered_pin = form.cleaned_data.get('pin')
            if entered_pin == account_details.pin:
                pin_validated = True  # PIN is validated, show deposit form
                deposit_form = AtmDepositForm()  # Initialize the deposit form without POST data
            else:
                pin_error = 'Incorrect PIN. Please try again.'

        elif 'submit_deposit' in request.POST:
            deposit_form = AtmDepositForm(request.POST)
            if deposit_form.is_valid():
                new_amount = deposit_form.cleaned_data.get('amount')
                if new_amount > 0:
                    if new_amount <= account_details.amount:  # Check if the amount is less than or equal to the available balance
                        with transaction.atomic():
                            # Update the account balance
                            account_details.amount -= new_amount
                            account_details.save()

                            # Save the transaction
                            transactions.objects.create(
                                account_number=account_details.account_number,
                                transaction_type='W',  # 'W' for Withdraw
                                amount=new_amount,
                                total_amount=account_details.amount,  # Store the updated balance
                                description='Withdraw via ATM'
                            )

                        # Redirect to the ATM options page after a successful withdrawal
                        return redirect('atm_options', generated_number=generated_number)
                    else:
                        pin_error = 'Insufficient funds. Please enter a smaller amount.'
                else:
                    pin_error = 'Amount must be positive.'
            else:
                pin_validated = True  # Ensure the deposit form is displayed again

    # Render the form if the PIN was validated
    if pin_validated and deposit_form is None:
        deposit_form = AtmDepositForm()

    return render(request, 'deposit.html', {
        'form': form,
        'deposit_form': deposit_form,
        'pin_error': pin_error,
        'pin_validated': pin_validated,
        'generated_number': generated_number,
    })

def view_transactions(request):
    form = AccountNumberForm(request.POST or None)
    transaction = None
    error = None

    if request.method == 'POST':
        if form.is_valid():
            account_number = form.cleaned_data['account_number'].strip()
            try:
                # Ensure the account exists
                account_obj = account.objects.get(account_number=account_number)
                
                # Fetch all transactions related to the account, ordered from oldest to newest
                transaction = transactions.objects.filter(account_number=account_number).order_by('date')
            except account.DoesNotExist:
                error = 'Account number does not exist'

    return render(request, 'view_transactions.html', {
        'form': form,
        'transaction': transaction,
        'error': error
    })