# Generated by Django 5.1.1 on 2024-11-01 10:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_userstatistics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biddingwinner',
            name='winning_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]