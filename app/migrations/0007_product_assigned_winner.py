# Generated by Django 5.1.1 on 2024-11-01 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_biddingwinner_winning_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='assigned_winner',
            field=models.BooleanField(default=False),
        ),
    ]
