from django import forms
from .models import account

class accountForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(label="I accept the terms and conditions", required=True)
    
    class Meta:
        model = account
        fields = ['name', 'age', 'email', 'phone', 'address', 'gender', 'photo', 'date', 'terms_accepted']
