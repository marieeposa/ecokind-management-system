from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Profile, Supplier, Customer

@admin.register(Profile)
class ProfileAdmin(SimpleHistoryAdmin):
    list_display = ('user', 'telephone', 'email', 'role', 'status')

@admin.register(Supplier)
class SupplierAdmin(SimpleHistoryAdmin):
    fields = ('name', 'phone_number', 'email', 'address_line_one', 'city', 'province', 'zip_code', 'country')
    list_display = ('name', 'phone_number', 'email', 'address_line_one', 'city', 'province', 'zip_code', 'country')
    search_fields = ['name', 'phone_number', 'email', 'address_line_one', 'city', 'province', 'zip_code', 'country']

@admin.register(Customer)
class CustomerAdmin(SimpleHistoryAdmin):
    fields = ('company', 'first_name', 'last_name', 'email_address', 'street', 'barangay', 'city', 'zip_code', 'province', 'country')
    list_display = ('first_name', 'last_name', 'email_address', 'company', 'city', 'province', 'country')
    search_fields = ['first_name', 'last_name', 'email_address', 'company', 'city', 'province', 'country']
