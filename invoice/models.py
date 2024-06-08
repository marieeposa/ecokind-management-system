from django.db import models
from transactions.models import Sale
from django.utils import timezone
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteObject

class Invoice(SoftDeleteObject, models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()

    def __str__(self):
        return f"Invoice {self.id} for Sale {self.sale.id}"
