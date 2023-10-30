from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from shop.models import User, Purchase, Product


class PurchaseValidationException(Exception):
    pass


class UserCreateForm(UserCreationForm):
    image = forms.FileField(label='Image', max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'image']


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PurchaseCreateForm(forms.ModelForm):
    product_quantity = forms.IntegerField(label='Quantity', initial=1, min_value=1, required=True,
                                          widget=forms.NumberInput)

    class Meta:
        model = Purchase
        fields = ['product_quantity']

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        if 'product_pk' in kwargs:
            self.product_pk = kwargs.pop('product_pk')
        self.product = kwargs.pop('product', None)
        self.user = kwargs.pop('user', None)
        super(PurchaseCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        try:
            product = Product.objects.get(pk=self.product_pk)

            if self.request.user.wallet < cleaned_data.get('product_quantity') * product.price:
                self.add_error(None,
                               'Insufficient balance error')
                messages.error(self.request,
                               "Sorry, it looks like you don't have sufficient funds to complete this transaction.")
                raise PurchaseValidationException("Insufficient balance error")

            if cleaned_data.get('product_quantity') > product.quantity:
                self.add_error(None, 'Error')
                messages.error(self.request,
                               "The quantity you've specified exceeds the current available stock. Please review your \
                               order and adjust the quantity accordingly to ensure we can fulfill your request.")
                raise PurchaseValidationException("Quantity exceeds stock error")

        except Product.DoesNotExist:
            self.add_error(None, 'Error')
            messages.error(self.request,
                           "Sorry, it seems that the requested product is currently unavailable or does not exist in \
                           our inventory. Please double-check the product details or explore our other offerings.")
            raise PurchaseValidationException("Product not found error")
