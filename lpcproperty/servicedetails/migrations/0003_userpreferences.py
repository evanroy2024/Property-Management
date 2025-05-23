# Generated by Django 5.1.7 on 2025-04-03 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_vendor'),
        ('servicedetails', '0002_remove_servicerequest_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('arrival_date', models.DateField()),
                ('arrival_time', models.TimeField()),
                ('temperature', models.FloatField()),
                ('pool_temperature', models.FloatField()),
                ('hot_bath_temperature', models.FloatField()),
                ('indoor_lights', models.CharField(choices=[('all_on', 'All On'), ('all_off', 'All Off')], max_length=10)),
                ('outdoor_lights', models.CharField(choices=[('all_on', 'All On'), ('all_off', 'All Off')], max_length=10)),
                ('window_position', models.CharField(choices=[('up', 'Up'), ('down', 'Down'), ('sideway', 'Sideway')], max_length=10)),
                ('music_genre', models.CharField(max_length=255)),
                ('flower_type', models.CharField(max_length=255)),
                ('flower_location', models.CharField(max_length=255)),
                ('groceries_details', models.TextField()),
                ('alcohol', models.TextField()),
                ('housekeeping', models.TextField()),
                ('transportation', models.TextField()),
                ('automobiles', models.TextField()),
                ('additional', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.client')),
            ],
        ),
    ]
