# Generated by Django 3.2.7 on 2021-09-14 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('akart', '0012_alter_ordertracker_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertracker',
            name='order_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='akart.orderdetails'),
        ),
    ]