# Generated by Django 3.1.7 on 2021-04-18 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reviews',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]