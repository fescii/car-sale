from django import forms
from django.contrib.auth.models import User
from .models import Profile
from carinfo.models import Car
from django.forms import ModelChoiceField


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_type', 'photo']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'model', 'location', 'image', 'year', 'price', 'location', 'notes']

class SearchForm(forms.Form):
    model = forms.ModelChoiceField(Car.objects.values_list('model', flat=True).distinct(), initial=0)
    location = forms.ModelChoiceField(queryset=Car.objects.values_list('location', flat=True).distinct(), initial=0)
