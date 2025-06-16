from django import forms
    
class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        help_text='Your full name.'
    )
    email = forms.EmailField()

    address = forms.CharField(
        max_length=100,
        help_text='Your address.'
    )

    city = forms.CharField(
        max_length=150,
        help_text='Your city.'
    )

    postal_code = forms.CharField(
        max_length=20,
        help_text='Your postal code.'
    )