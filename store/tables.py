# tutorial/tables.py
import django_tables2 as tables
from .models import Item, Delivery, Customer

class ItemTable(tables.Table):
    class Meta:
        model = Item
        template_name = "django_tables2/semantic.html"
        fields = ('id', 'name', 'category', 'quantity', 'selling_price', 'expiring_date', 'supplier')
        order_by_field = 'sort'

class DeliveryTable(tables.Table):
    class Meta:
        model = Delivery
        template_name = "django_tables2/bootstrap.html"
        fields = ('pk_logistics_id', 'company', 'contact_number', 'email_address', 'street', 'barangay', 'city', 'zip_code', 'province', 'country')

class CustomerTable(tables.Table):
    class Meta:
        model = Customer
        template_name = "django_tables2/bootstrap4.html"
        fields = ("customer_id", "company", "first_name", "last_name", "email_address", "street", "barangay", "city", "zip_code", "province", "country")
        sequence = ("customer_id", "company", "first_name", "last_name", "email_address", "street", "barangay", "city", "zip_code", "province", "country")
        order_by = "customer_id"