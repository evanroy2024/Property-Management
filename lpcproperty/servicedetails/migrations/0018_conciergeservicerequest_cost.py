# Generated by Django 5.1.7 on 2025-07-09 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicedetails', '0017_alter_servicerequest_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='conciergeservicerequest',
            name='cost',
            field=models.BigIntegerField(default=0),
        ),
    ]
