from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField
from django_extensions.db.fields import AutoSlugField
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteObject

STATUS_CHOICES = [
    ('INA', 'Inactive'),
    ('A', 'Active'),
    ('OL', 'On_leave')
]

ROLE_CHOICES = [
    ('OP', 'Operative'),
    ('EX', 'Executive'),
    ('AD', 'Admin')
]

class Profile(SoftDeleteObject, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = AutoSlugField(unique=True, verbose_name=('Account ID'), populate_from='user__email')
    profile_picture = ProcessedImageField(default='profile_pics/default.jpg', upload_to='profile_pics', format='JPEG',
                                          processors=[ResizeToFill(150, 150)],
                                          options={'quality': 100})
    telephone = PhoneNumberField(null=True, blank=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=12, blank=False, null=False, default='INA')
    role = models.CharField(choices=ROLE_CHOICES, max_length=12, blank=True, null=True)
    history = HistoricalRecords()

    @property
    def imageURL(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''
        return url

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        ordering = ["slug"]

class Supplier(SoftDeleteObject, models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(unique=True, populate_from='name')
    phone_number = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address_line_one = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Customer(SoftDeleteObject, models.Model):
    customer_id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(unique=True)
    street = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['last_name', 'first_name']

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new record
            if Customer.objects.count() == 0:  # No existing records
                self.customer_id = 1
            else:
                last_customer = Customer.objects.order_by('-customer_id').first()
                self.customer_id = last_customer.customer_id + 1
        super().save(*args, **kwargs)
