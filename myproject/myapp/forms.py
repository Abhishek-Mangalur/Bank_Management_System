from django import forms
from .models import Account, Loan, FixedDeposit

class AccountForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(label="I accept the terms and conditions", required=True)
    
    class Meta:
        model = Account
        fields = ['fname', 'lname', 'age', 'email', 'phone', 'address', 'gender', 'photo', 'date', 'amount', 'terms_accepted']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Renders the date field as a date picker
        }

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['amount'].initial = None  # This makes the amount field empty by default
        self.fields['amount'].widget.attrs['placeholder'] = ''  # Optional: Adds an empty placeholder

class EditForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(label="I accept the terms and conditions", required=True)
    
    class Meta:
        model = Account  # Ensure this matches your model name
        fields = ['account_number', 'fname', 'lname', 'age', 'email', 'phone', 'address', 'gender', 'photo', 'terms_accepted']

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        # Disable the account_number field
        self.fields['account_number'].disabled = True

class EmailForm(forms.Form):
    email = forms.EmailField()

class AccountNumberForm(forms.Form):
    account_number = forms.CharField(max_length=20)

class DepositeForm(forms.Form):
    account_number = forms.CharField(max_length=20, label='')

class UpdateAmountForm(forms.Form):
    account_number = forms.CharField(max_length=20, widget=forms.HiddenInput())
    new_amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Enter Amount')

    def clean_new_amount(self):
        new_amount = self.cleaned_data.get('new_amount')
        if new_amount < 0:
            raise forms.ValidationError("The amount cannot be negative.")
        return new_amount

class NumberForm(forms.Form):
    generated_number = forms.CharField(max_length=20, label='')

class PinForm(forms.Form):
    pin = forms.CharField(required=False)  # Set required to False

    def __init__(self, *args, **kwargs):
        super(PinForm, self).__init__(*args, **kwargs)
        self.fields['pin'].label = ""  # Remove label


class AtmDepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='')

class LoanAccountNumberForm(forms.Form):
    account_number = forms.CharField(
        max_length=14,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Account Number',
            'class': 'form-control',
        }),
        label=''  # No label, just a clean input field
    )

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['loan_amount', 'tenure', 'interest_rate', 'reason']

    def __init__(self, *args, **kwargs):
        account_instance = kwargs.pop('account_instance', None)
        super(LoanForm, self).__init__(*args, **kwargs)
        if account_instance:
            # Set the account_number field with a custom label (account_number)
            self.fields['account_number'] = forms.ModelChoiceField(
                queryset=account.objects.filter(pk=account_instance.pk),
                initial=account_instance,
                widget=forms.TextInput(attrs={'readonly': 'readonly'})
            )
            self.fields['account_number'].label_from_instance = lambda obj: obj.account_number

class PayLoanForm(forms.Form):
    payed_loan = forms.DecimalField(max_digits=10, decimal_places=2)
    reason = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        account_number = kwargs.pop('account_number', None)
        super().__init__(*args, **kwargs)
        if account_number:
            # Update queryset based on account_number
            reasons = Loan.objects.filter(account_number=account_number).values_list('reason', flat=True).distinct()
            self.fields['reason'].choices = [(reason, reason) for reason in reasons]

class LoanSelectForm(forms.Form):
    reason = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        account_number = kwargs.pop('account_number', None)
        super().__init__(*args, **kwargs)
        if account_number:
            # Update queryset based on account_number
            reasons = Loan.objects.filter(account_number=account_number).values_list('reason', flat=True).distinct()
            self.fields['reason'].choices = [(reason, reason) for reason in reasons]

class FixedDepositForm(forms.ModelForm):
    class Meta:
        model = FixedDeposit
        fields = ['principal_amount', 'interest_rate', 'start_date', 'maturity_date']

class FDAccountNumberForm(forms.Form):
    account_number = forms.CharField(max_length=14, label='Account Number')
