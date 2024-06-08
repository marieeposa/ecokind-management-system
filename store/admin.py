from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Category, Delivery, Item

@admin.register(Item)
class ItemAdmin(SimpleHistoryAdmin):
    fields = ('name', 'category', 'quantity', 'selling_price', 'expiring_date', 'supplier')
    list_display = ('id', 'name', 'category', 'quantity', 'selling_price', 'expiring_date', 'supplier')
    search_fields = ['id', 'name']

@admin.register(Category)
class CategoryAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']

@admin.register(Delivery)
class DeliveryAdmin(SimpleHistoryAdmin):
    list_display = ['company', 'city', 'province', 'country']
    search_fields = ['company', 'city', 'province', 'country']
