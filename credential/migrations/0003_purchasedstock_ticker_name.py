# Generated by Django 4.2.2 on 2023-07-04 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credential', '0002_rename_average_cost_stock_average_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasedstock',
            name='ticker_name',
            field=models.CharField(default='ticker', max_length=100),
        ),
    ]
