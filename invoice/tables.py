import django_tables2 as tables
from .models import Invoice
from django.shortcuts import render

class InvoiceTable(tables.Table):
    sales_order = tables.Column(accessor='sale.id', verbose_name='Sales Order ID')

    class Meta:
        model = Invoice
        template_name = 'django_tables2/bootstrap.html'
        fields = ('invoice_id', 'sales_order', 'customer_name', 'shipping_fee', 'subtotal', 'total_amount_due')
        sequence = ('invoice_id', 'sales_order', 'customer_name', 'shipping_fee', 'subtotal', 'total_amount_due')