# Generated by Django 4.1.7 on 2023-04-05 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_order_ordered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateField(),
        ),
    ]
