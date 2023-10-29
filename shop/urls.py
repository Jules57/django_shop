from django.contrib.auth.views import LogoutView
from django.urls import path

from shop.views import Login, UserRegisterView, ProductListView, ProductDetailView, ProductCreate, ProductUpdate

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreate.as_view(), name='add_product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/update/', ProductUpdate.as_view(), name='update_product'),
    # path('product/<int:pk>/delete/', ProductDelete.as_view(), name='delete_product'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),

]
