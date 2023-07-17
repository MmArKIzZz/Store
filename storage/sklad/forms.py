from django import forms
from captcha.fields import CaptchaField

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()

class YourForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
