# Generated by Django 5.1.1 on 2024-10-14 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_bidding_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidding',
            name='contact_no',
        ),
    ]
