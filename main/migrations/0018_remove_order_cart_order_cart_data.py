# Generated by Django 5.1.3 on 2025-01-07 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_order_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.AddField(
            model_name='order',
            name='cart_data',
            field=models.JSONField(default='e'),
        ),
    ]
