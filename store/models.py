from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import Supplier, Customer
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteObject

class Category(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(unique=True, populate_from='name')
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Categories'

class Item(SoftDeleteObject, models.Model):
    slug = AutoSlugField(unique=True, populate_from='name')
    name = models.CharField(max_length=50, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.00)
    selling_price = models.FloatField(default=0)
    expiring_date = models.DateTimeField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    reorder_point = models.IntegerField(default=10)
    reorder_status = models.CharField(max_length=10, default='OK')
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} - Category: {self.category}, Quantity: {self.quantity}"

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.quantity < self.reorder_point:
            self.reorder_status = 'Reorder'
        else:
            self.reorder_status = 'OK'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Items"

class Delivery(SoftDeleteObject, models.Model):
    """
    Represents a delivery of an item to a customer.
    """
    pk_logistics_id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=255, default='Unknown')
    contact_number = PhoneNumberField(default='N/A')
    email_address = models.EmailField(default='N/A')
    street = models.CharField(max_length=255, default='Unknown')
    barangay = models.CharField(max_length=100, default='Unknown')
    city = models.CharField(max_length=255, default='Unknown')
    zip_code = models.CharField(max_length=10, default='Unknown')
    province = models.CharField(max_length=255, default='Unknown')
    country = models.CharField(max_length=255, default='Unknown')
    history = HistoricalRecords()

    def __str__(self):
        return (
            f"Delivery from {self.company} "
            f"to {self.city}, {self.province}, {self.country}"
        )
