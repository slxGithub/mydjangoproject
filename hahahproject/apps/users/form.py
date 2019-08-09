from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=6)

class RegisterForm(forms.Form):
    email = forms.CharField(required=True,max_length=20)
    password = forms.CharField(required=True,min_length=6)
    captcha = CaptchaField(required=True,error_messages={'invalid': '验证码错误'})