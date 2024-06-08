# Generated by Django 5.0.4 on 2024-05-28 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=254, unique=True)),
                ('street', models.CharField(max_length=100)),
                ('barangay', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=20)),
                ('province', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
    ]
