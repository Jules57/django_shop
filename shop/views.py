from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
# from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from shop.forms import UserCreateForm, UserLoginForm
from shop.models import Product


class Login(LoginView):
    success_url = '/'
    template_name = 'shop/user/login.html'

    def get_success_url(self):
        return self.success_url


class UserRegisterView(CreateView):
    template_name = 'shop/user/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('shop:product_list')


class ProductListView(ListView):
    model = Product
    paginate_by = 5
    template_name = 'shop/product/list.html'
    ordering = ['title']


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'


class ProductUpdate(UpdateView):
    model = Product
    fields = ['title', 'description', 'quantity', 'price', 'image']
    template_name = 'shop/product/product_update_form.html'


class ProductCreate(CreateView):
    template_name = 'shop/product/product_create.html'
    model = Product
    fields = ['title', 'description', 'quantity', 'price', 'image']
