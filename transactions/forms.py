# transactions/forms.py
from django import forms
from django.forms import ModelChoiceField
from .models import PurchaseOrder, PurchaseOrderDetail, Sale, Customer, Delivery, SalesOrderDetail, Item

class CustomerChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.customer_id} - {obj.first_name} {obj.last_name}"

class LogisticsChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.pk_logistics_id} - {obj.company}"

class SaleForm(forms.ModelForm):
    customer_id = CustomerChoiceField(queryset=Customer.objects.all().order_by('last_name', 'first_name'), label="Customer")
    logistics_id = LogisticsChoiceField(queryset=Delivery.objects.all(), label="Logistics")

    class Meta:
        model = Sale
        fields = [
            'customer_id', 'logistics_id', 'order_type', 'delivery_date',
            'sales_order_status', 'payment_type', 'shipping_fee'
        ]
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SalesOrderDetailForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        label="Item",
        empty_label=None
    )

    class Meta:
        model = SalesOrderDetail
        fields = ['item', 'description', 'quantity']

    def __init__(self, *args, **kwargs):
        super(SalesOrderDetailForm, self).__init__(*args, **kwargs)
        self.fields['item'].label_from_instance = lambda obj: f"{obj.name}"

# Keep the rest of your forms unchanged
class SalesOrderDetailForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        label="Item",
        empty_label=None
    )

    class Meta:
        model = SalesOrderDetail
        fields = ['item', 'description', 'quantity']

    def __init__(self, *args, **kwargs):
        super(SalesOrderDetailForm, self).__init__(*args, **kwargs)
        self.fields['item'].label_from_instance = lambda obj: f"{obj.name}"

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = [
            'supplier_id', 'order_date', 'delivery_date', 'delivery_status',
            'payment_method', 'payment_status', 'total_amount_due'
        ]
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'total_amount_due': forms.HiddenInput(),  # Hide this field
        }

class PurchaseOrderDetailForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderDetail
        fields = ['item', 'description', 'quantity', 'unit_price']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
