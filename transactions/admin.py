from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import PurchaseOrder, PurchaseOrderDetail, Sale, SalesOrderDetail

# Registering the PurchaseOrder and PurchaseOrderDetail models
admin.site.register(PurchaseOrder, SimpleHistoryAdmin)
admin.site.register(PurchaseOrderDetail, SimpleHistoryAdmin)

@admin.register(Sale)
class SaleAdmin(SimpleHistoryAdmin):
    fields = ('customer_id', 'logistics_id', 'order_type', 'order_date', 'delivery_date', 
              'sales_order_status', 'total_amount_due', 'payment_type', 'payment_status', 'items')
    list_display = ('id', 'slug', 'customer_id', 'logistics_id', 'order_type', 'order_date', 'delivery_date', 
                    'sales_order_status', 'total_amount_due', 'payment_type', 'payment_status', 'items')

# Optional: Register SalesOrderDetail if needed in admin
@admin.register(SalesOrderDetail)
class SalesOrderDetailAdmin(SimpleHistoryAdmin):
    list_display = ('sale', 'item', 'description', 'quantity', 'selling_price', 'subtotal')
    fields = ('sale', 'item', 'description', 'quantity', 'selling_price', 'subtotal')
