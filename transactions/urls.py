# transactions/urls.py
from django.urls import path
from . import views
from .views import get_sales_orders_data
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    PurchaseOrderListView,
    PurchaseOrderCreateView,
    PurchaseOrderDetailView,
    PurchaseOrderUpdateView,
    PurchaseOrderDeleteView,
    PurchaseOrderDetailViewList,
    PurchaseOrderDetailCreateView,
    PurchaseOrderDetailUpdateView,
    PurchaseOrderDetailDeleteView,
    SaleListView,
    SaleDetailView,
    SaleCreateView,
    SaleUpdateView,
    SaleDeleteView,
    SalesOrderDetailViewList,
    SalesOrderDetailCreateView,
    SalesOrderDetailUpdateView,
    SalesOrderDetailDeleteView,
    generate_invoice_view
)

urlpatterns = [
    path('purchases/', PurchaseOrderListView.as_view(), name='purchases_list'),
    path('purchases/create/', PurchaseOrderCreateView.as_view(), name='purchases_create'),
    path('purchases/<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchases_detail'),
    path('purchases/<int:pk>/update/', PurchaseOrderUpdateView.as_view(), name='purchases_update'),
    path('purchases/<int:pk>/delete/', PurchaseOrderDeleteView.as_view(), name='purchases_delete'),
    path('purchases/<int:pk>/items/', PurchaseOrderDetailViewList.as_view(), name='purchases_detail_view'),
    path('purchases/<int:pk>/items/add/', PurchaseOrderDetailCreateView.as_view(), name='purchases_detail_create'),
    path('purchases/<int:order_pk>/items/<int:pk>/edit/', PurchaseOrderDetailUpdateView.as_view(), name='purchase_detail_update'),
    path('purchases/<int:order_pk>/items/<int:pk>/delete/', PurchaseOrderDetailDeleteView.as_view(), name='purchase_detail_delete'),
    path('sales/', SaleListView.as_view(), name='saleslist'),
    path('sale/<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
    path('new-sale/', SaleCreateView.as_view(), name='sale-create'),
    path('sale/<int:pk>/update/', SaleUpdateView.as_view(), name='sale-update'),
    path('sale/<int:pk>/delete/', SaleDeleteView.as_view(), name='sale-delete'),
    # URLs for SalesOrderDetail
    path('sales/<int:sale_id>/items/', SalesOrderDetailViewList.as_view(), name='salesitems-list'),
    path('sales/<int:sale_id>/items/add/', SalesOrderDetailCreateView.as_view(), name='sales-order-detail-add'),
    path('sales/<int:sale_id>/items/<int:pk>/edit/', SalesOrderDetailUpdateView.as_view(), name='sales-order-detail-edit'),
    path('sales/<int:sale_id>/items/<int:pk>/delete/', SalesOrderDetailDeleteView.as_view(), name='sales-order-detail-delete'),
    path('generate-invoice/', generate_invoice_view, name='generate-invoice'),
    path('api/sales-orders/', get_sales_orders_data, name='api-sales-orders'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
