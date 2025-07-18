# Generated by Django 5.1.7 on 2025-06-20 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicedetails', '0009_departureinformation_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicerequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('open', 'Open'), ('completed', 'Completed'), ('denied', 'Denied')], default='open', max_length=10),
        ),
    ]
