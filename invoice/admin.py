from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(SimpleHistoryAdmin):
    fields = ('sale', 'date')
    list_display = ('id', 'sale', 'customer_name', 'date')

    def customer_name(self, obj):
        return f"{obj.sale.customer_id.first_name} {obj.sale.customer_id.last_name}"

    customer_name.short_description = 'Customer Name'
