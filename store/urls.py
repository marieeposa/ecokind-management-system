from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import get_product_stock_data

from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ItemSearchListView,
    DeliveryListView,
    DeliveryDetailView,
    DeliveryCreateView,
    DeliveryUpdateView,
    DeliveryDeleteView,
    SupplierListView,
    SupplierCreateView,
    SupplierUpdateView,
    SupplierDeleteView,
    CustomerListView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView
)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', ProductListView.as_view(), name="productslist"),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('new-product/', ProductCreateView.as_view(), name='product-create'),
    path('product/<slug:slug>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('search/', ItemSearchListView.as_view(), name="item_search_list_view"),

    path('deliveries/', DeliveryListView.as_view(), name='deliveries'),
    path('delivery/<int:pk>/', DeliveryDetailView.as_view(), name='delivery-detail'),
    path('new-delivery/', DeliveryCreateView.as_view(), name='delivery-create'),
    path('delivery/<int:pk>/update/', DeliveryUpdateView.as_view(), name='delivery-update'),
    path('delivery/<int:pk>/delete/', DeliveryDeleteView.as_view(), name='delivery-delete'),

    path('suppliers/', SupplierListView.as_view(), name="suppliers"),
    path('supplier/create/', SupplierCreateView.as_view(), name="supplier-create"),
    path('supplier/<int:pk>/update/', SupplierUpdateView.as_view(), name='supplier-update'),
    path('supplier/<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier-delete'),

    path('customers/', CustomerListView.as_view(), name="customers"),              # Added for Customer
    path('customer/<int:pk>/', views.customer_detail, name='customer-detail'),
    path('customer/create/', CustomerCreateView.as_view(), name="customer-create"),# Added for Customer
    path('customer/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer-update'), # Added for Customer
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),  # Added for Customer
    path('customer/<int:pk>/', views.customer_detail, name='customer-detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
