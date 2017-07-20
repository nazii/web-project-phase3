from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
