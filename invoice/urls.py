# invoice/urls.py
from django.urls import path
from .views import generate_invoice_view, invoice_list_view, invoice_detail_view, delete_invoice_view

urlpatterns = [
    path('generate/', generate_invoice_view, name='generate-invoice'),
    path('list/', invoice_list_view, name='invoice-list'),
    path('<int:pk>/', invoice_detail_view, name='invoice-detail'),
    path('<int:pk>/delete/', delete_invoice_view, name='delete-invoice'),
]
