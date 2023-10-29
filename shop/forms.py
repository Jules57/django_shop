from django.contrib.auth.forms import UserCreationForm
from django import forms

from shop.models import User


class UserCreateForm(UserCreationForm):
    image = forms.FileField(label='Image', max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'image']


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
