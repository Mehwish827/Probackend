# Generated by Django 5.2.3 on 2025-06-29 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0032_userbooking_delete_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbooking',
            name='coupon',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
