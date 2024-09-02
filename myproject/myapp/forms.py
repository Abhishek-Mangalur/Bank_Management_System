from django import forms
from .models import account

class accountForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(label="I accept the terms and conditions", required=True)
    
    class Meta:
        model = account
        fields = ['fname', 'lname', 'age', 'email', 'phone', 'address', 'gender', 'photo', 'date', 'amount', 'terms_accepted']

class editForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(label="I accept the terms and conditions", required=True)
    
    class Meta:
        model = account  # Ensure this matches your model name
        fields = ['account_number', 'fname', 'lname', 'age', 'email', 'phone', 'address', 'gender', 'photo', 'terms_accepted']

    def __init__(self, *args, **kwargs):
        super(editForm, self).__init__(*args, **kwargs)
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
    new_amount = forms.DecimalField(max_digits=10, decimal_places=2, label='New Amount')

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
