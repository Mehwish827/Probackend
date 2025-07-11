# Generated by Django 5.2.3 on 2025-06-29 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0034_userbooking_plot_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cnic', models.CharField(max_length=20, unique=True)),
                ('coupon_id', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
