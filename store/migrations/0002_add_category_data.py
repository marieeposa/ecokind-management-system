from django.db import migrations

def add_category_data(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    categories_to_add = [
        "Shampoos and Conditioners",
        "Soaps and Gels",
        "Body Care",
        "Waxes",
        "Dental Kits",
        "Vanity Kits",
    ]
    for category_name in categories_to_add:
        # This ensures a category is created only if it does not already exist.
        if not Category.objects.filter(name=category_name).exists():
            Category.objects.create(name=category_name)

class Migration(migrations.Migration):
    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_category_data),
    ]