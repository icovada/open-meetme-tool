from allauth.account.forms import LoginForm, SignupForm
from django import forms

BOOTSTRAP5_TEXT_CLASS = 'form-control'

# Personal note: https://builtwithdjango.com/blog/styling-authentication-pages
class BSSignupForm(SignupForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    company = forms.CharField(max_length=30, label='Company')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': BOOTSTRAP5_TEXT_CLASS})
        self.fields['first_name'].widget = forms.TextInput(
            attrs={'class': BOOTSTRAP5_TEXT_CLASS})
        self.fields['last_name'].widget = forms.TextInput(
            attrs={'class': BOOTSTRAP5_TEXT_CLASS})
        self.fields['company'].widget = forms.TextInput(
            attrs={'class': BOOTSTRAP5_TEXT_CLASS})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': BOOTSTRAP5_TEXT_CLASS})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': BOOTSTRAP5_TEXT_CLASS})


    def save(self, request):
        user = super().save(request)
        user.company = self.cleaned_data['company']
        user.username = self.cleaned_data['email']
        user.save()
        return user


class BSLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget = forms.EmailInput(
            attrs={'class': BOOTSTRAP5_TEXT_CLASS})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': BOOTSTRAP5_TEXT_CLASS})
        self.fields['remember'].widget = forms.CheckboxInput(
            attrs={'class': 'form-check-input'})