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
