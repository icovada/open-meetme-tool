from allauth.account.forms import SignupForm, LoginForm
from django import forms

BOOTSTRAP5_TEXT_CLASS = 'form-control'

class SimpleSignupForm(SignupForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    company = forms.CharField(max_length=30, label='Company')

    def save(self, request):
        user = super(SimpleSignupForm, self).save(request)
        user.company = self.cleaned_data['company']
        user.username = self.cleaned_data['email']
        user.save()
        return user


class BSLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(
            attrs={'type': 'email', 'class': BOOTSTRAP5_TEXT_CLASS})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': BOOTSTRAP5_TEXT_CLASS})
        self.fields['remember'].widget = forms.CheckboxInput(
            attrs={'class': 'form-check-input'})
