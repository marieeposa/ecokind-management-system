# Generated by Django 5.0.4 on 2024-06-02 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_alter_purchaseorder_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='total_amount_due',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
