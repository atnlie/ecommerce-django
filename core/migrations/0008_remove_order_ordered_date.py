# Generated by Django 4.1.7 on 2023-04-05 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_item_quantity_orderitem_ordered_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ordered_date',
        ),
    ]
