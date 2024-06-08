from django.db import models
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField
from django.db.models import Sum
from accounts.models import Customer, Supplier
from store.models import Item, Delivery
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteObject

class Sale(SoftDeleteObject, models.Model):
    def get_customer_name(self):
        if self.customer_id:
            return f"{self.customer_id.first_name} {self.customer_id.last_name}"
        return ""

    slug = AutoSlugField(unique=True, populate_from='get_customer_name')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    logistics_id = models.ForeignKey(Delivery, on_delete=models.CASCADE, null=True, blank=True)
    order_type = models.CharField(max_length=50, choices=[
        ('Online Order', 'Online Order'), 
        ('In-person Transaction', 'In-person Transaction')
    ], null=True, blank=True)
    order_date = models.DateField(default=timezone.now)
    delivery_date = models.DateField(null=True, blank=True)
    sales_order_status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'), 
        ('Placed', 'Placed'), 
        ('Shipped', 'Shipped'), 
        ('Delivered', 'Delivered'), 
        ('Cancelled', 'Cancelled')
    ], null=True, blank=True)
    total_amount_due = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_type = models.CharField(max_length=50, choices=[
        ('Cash', 'Cash'), 
        ('Debit Card', 'Debit Card'), 
        ('Bank Transfer', 'Bank Transfer'), 
        ('Gcash', 'Gcash')
    ], null=True, blank=True)
    payment_status = models.CharField(max_length=50, choices=[
        ('Paid', 'Paid'), 
        ('Unpaid', 'Unpaid'),
    ], null=True, blank=True)
    items = models.IntegerField(null=True, blank=True)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Shipping fee for the order")
    history = HistoricalRecords()

    def __str__(self):
        return f"Sale Order {self.slug}"

    def update_total_amount_due(self):
        item_total = self.order_details.aggregate(total=Sum('subtotal'))['total'] or 0
        self.total_amount_due = item_total + self.shipping_fee
        self.save()

class SalesOrderDetail(SoftDeleteObject, models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='order_details')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.selling_price = self.item.selling_price
        self.subtotal = self.quantity * self.selling_price
        super().save(*args, **kwargs)
        self.sale.update_total_amount_due()

    def __str__(self):
        return f'{self.item.name} - {self.quantity} * {self.selling_price}'

class PurchaseOrder(SoftDeleteObject, models.Model):
    purchase_order_id = models.AutoField(primary_key=True)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateField()
    delivery_date = models.DateField()
    DELIVERY_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Placed', 'Placed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES)
    total_amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Debit Card', 'Debit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Gcash', 'Gcash')
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
        ('Partially Paid', 'Partially Paid')
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    items = models.IntegerField(default=0)
    history = HistoricalRecords()

    def __str__(self):
        return f'Purchase Order {self.purchase_order_id}'

class PurchaseOrderDetail(SoftDeleteObject, models.Model):
    purchase_order_details_id = models.AutoField(primary_key=True)
    purchase_order_id = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Purchase Order Detail {self.purchase_order_details_id}'
