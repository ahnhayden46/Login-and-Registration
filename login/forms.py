from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import Widget
from .models import *
from .utils import *


class EvaluationForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ['description', 'image']


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email])
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class CreateCustomerForm(ModelForm):
    contact_number = forms.CharField(required=True, max_length=11)

    class Meta:
        model = Customer
        fields = ['contact_number']
