# Generated by Django 5.1.7 on 2025-05-11 15:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propertydetails', '0015_propertymanagement_zipcode'),
        ('walkthroughreport', '0017_walkthroughreport_bathroom5_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='walkthroughreport',
            name='property',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='propertydetails.propertymanagement'),
        ),
    ]
