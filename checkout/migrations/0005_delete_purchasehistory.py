# Generated by Django 5.0.6 on 2024-05-18 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_payment_country_payment_county_payment_email_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PurchaseHistory',
        ),
    ]