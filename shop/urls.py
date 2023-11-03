from django.contrib.auth.views import LogoutView
from django.urls import path

from shop.views import Login, UserRegisterView, ProductListView, ProductDetailView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView, PurchaseCreateView, PurchaseListView, ReturnCreateView, ReturnApproveView, \
    ReturnDeleteView, ReturnListView

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='update_product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('purchase/<int:pk>/', PurchaseCreateView.as_view(), name='purchase'),
    path('purchases/', PurchaseListView.as_view(), name='purchase_list'),
    path('purchases/<int:pk>/return/', ReturnCreateView.as_view(), name='create_return'),
    path('returns/', ReturnListView.as_view(), name='return_list'),
    path('returns/<int:pk>/approve/', ReturnApproveView.as_view(), name='approve_return'),
    path('returns/<int:pk>/decline/', ReturnDeleteView.as_view(), name='delete_return'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),

]
