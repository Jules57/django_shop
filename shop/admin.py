from django.contrib import admin
from .models import User, Product, Purchase, Return


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'wallet', 'image']
    list_filter = ['username', 'wallet']
    search_fields = ['username', 'last_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'quantity', 'image']
    list_filter = ['title', 'price', 'quantity']
    search_fields = ['title', 'price']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'product_quantity', 'bought_at']
    list_filter = ['user', 'product', 'bought_at']
    search_fields = ['product', 'user']
    date_hierarchy = 'bought_at'


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ['purchase', 'returned_at']
    list_filter = ['purchase', 'returned_at']
    search_fields = ['purchase', 'returned_at']
    date_hierarchy = 'returned_at'
