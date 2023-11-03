from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from shop.forms import UserCreateForm, PurchaseCreateForm
from shop.models import Product, Purchase, Return


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


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
    extra_context = {'purchase_form': PurchaseCreateForm()}


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'


class ProductUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Product
    fields = ['title', 'description', 'quantity', 'price', 'image']
    template_name = 'shop/product/product_update_form.html'


class ProductCreateView(SuperUserRequiredMixin, CreateView):
    template_name = 'shop/product/product_create.html'
    model = Product
    fields = ['title', 'description', 'quantity', 'price', 'image']


class ProductDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Product
    success_url = '/'
    template_name = 'shop/product/confirm_delete.html'


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    model = Purchase
    success_url = '/'
    form_class = PurchaseCreateForm
    http_method_names = ['post']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'product_pk': self.kwargs['pk'],
            'user': self.request.user
        })
        return kwargs

    def form_invalid(self, form):
        return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        obj = form.save(commit=False)
        product = Product.objects.get(pk=form.product_pk)
        obj.product = product
        obj.user = form.user
        product.quantity -= obj.product_quantity
        form.user.wallet -= product.price * obj.product_quantity
        with transaction.atomic():
            obj.save()
            product.save()
            self.request.user.save()
        messages.success(self.request, f"Your purchase of '{product.title}' has been successfully completed.")
        return super().form_valid(form=form)


class ReturnCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    model = Return
    success_url = '/'
    # form_class = PurchaseCreateForm
    # http_method_names = ['post']
