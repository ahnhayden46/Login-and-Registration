from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from django import forms
from .models import *
from .utils import *


class EvaluationForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ['description', 'image']


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateCustomerForm(forms.ModelForm):
    contact_number = forms.CharField(required=True, max_length=11)

    class Meta:
        model = Customer
        fields = ['contact_number']
