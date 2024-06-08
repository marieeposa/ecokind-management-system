from django import forms
from django.forms import ModelForm
from .models import Item, Supplier, Customer, Delivery

class ProductForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'quantity', 'selling_price', 'expiring_date', 'supplier']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Selling Price'}),
            'expiring_date': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'placeholder': 'mm/dd/yyyy'
            }),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone_number', 'email', 'address_line_one', 'city', 'province', 'zip_code', 'country']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'address_line_one': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line One'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Province'}),
            'zip_code': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company', 'first_name', 'last_name', 'email_address', 'street', 'barangay', 'city', 'zip_code', 'province', 'country']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'barangay': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Barangay'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'zip_code': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Province'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        }

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['company', 'contact_number', 'email_address', 'street', 'barangay', 'city', 'zip_code', 'province', 'country']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'barangay': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Barangay'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Province'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        }
