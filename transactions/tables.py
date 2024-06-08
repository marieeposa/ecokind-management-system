import django_tables2 as tables
from .models import Sale, PurchaseOrder, SalesOrderDetail

class SaleTable(tables.Table):
    action = tables.TemplateColumn(
        template_name='sales/actions_column.html', orderable=False, verbose_name='Actions'
    )

    class Meta:
        model = Sale
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'customer_id', 'logistics_id', 'order_type', 'order_date', 'delivery_date',
            'sales_order_status', 'total_amount_due', 'payment_type',
            'payment_status', 'items', 'action'
        )

class SalesOrderDetailTable(tables.Table):
    action = tables.TemplateColumn(
        template_name='sales/details_actions_column.html', orderable=False, verbose_name='Actions'
    )

    class Meta:
        model = SalesOrderDetail
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'item', 'description', 'quantity', 'selling_price', 'subtotal', 'action'
        )

class PurchaseOrderTable(tables.Table):
    class Meta:
        model = PurchaseOrder
        template_name = 'django_tables2/bootstrap.html'
        fields = (
            'supplier_id', 'order_date', 'delivery_date', 'delivery_status', 
            'total_amount_due', 'payment_method', 'payment_status', 'items'
        )
        order_by_field = 'sort'


