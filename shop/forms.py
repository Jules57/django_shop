import datetime

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms

from online_shop import settings
from shop.models import User, Purchase, Product, Return


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

            if cleaned_data.get('product_quantity') > product.quantity:
                self.add_error(None, 'Error')
                messages.error(self.request,
                               "The quantity you've specified exceeds the current available stock. Please review your \
                               order and adjust the quantity accordingly to ensure we can fulfill your request.")

        except Product.DoesNotExist:
            self.add_error(None, 'Error')
            messages.error(self.request,
                           "Sorry, it seems that the requested product is currently unavailable or does not exist in \
                           our inventory. Please double-check the product details or explore our other offerings.")


class ReturnCreateForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = []

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        if 'purchase_pk' in kwargs:
            self.purchase_pk = kwargs.pop('purchase_pk')
        super(ReturnCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        try:
            purchase = Purchase.objects.get(id=self.purchase_pk)
            bought_at = purchase.bought_at.replace(tzinfo=datetime.timezone.utc)
            datetime_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            return_time_limit = bought_at + datetime.timedelta(minutes=settings.ALLOWED_RETURN_TIME)

            if datetime_now > return_time_limit:
                self.add_error(None, 'Error')
                messages.error(self.request, 'Regrettably, the deadline for submitting your return order has lapsed.')

            if Return.objects.filter(id=self.request.POST.get('purchase_id')).exists():
                self.add_error(None, 'Error')
                messages.error(self.request, 'An existing purchase return has already been recorded."')
            else:
                self.purchase = purchase

        except Purchase.DoesNotExist:
            self.add_error(None, 'Error')
            messages.error(self.request, 'Purchase does not exist.')

    def save(self, commit=True):
        Return.objects.create(purchase=self.purchase)
        messages.success(self.request, "Your return request has been successfully submitted.")
