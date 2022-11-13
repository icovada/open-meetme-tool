from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser

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
