# Generated by Django 5.1.7 on 2025-06-25 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('walkthroughreport', '0025_walkthroughreport_bathroom10_10_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='walkthroughreport',
            name='client_approval',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Provided', 'Provided'), ('Denied', 'Denied')], default='Pending', max_length=10),
        ),
    ]
