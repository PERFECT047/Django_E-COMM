# Generated by Django 3.1.7 on 2021-04-20 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_auto_20210418_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='latitude',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='longitude',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
