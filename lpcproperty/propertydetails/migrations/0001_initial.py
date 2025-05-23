# Generated by Django 5.1.7 on 2025-04-02 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainapp', '0002_clientmanager_clientmanagers'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyManagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('size_of_home', models.CharField(max_length=50)),
                ('number_of_stories', models.PositiveIntegerField()),
                ('construction_type', models.CharField(max_length=100)),
                ('year_built', models.PositiveIntegerField()),
                ('has_pool', models.BooleanField(default=False)),
                ('gated_community', models.BooleanField(default=False)),
                ('impact_windows', models.BooleanField(default=False)),
                ('has_hoa', models.BooleanField(default=False)),
                ('gated_property', models.BooleanField(default=False)),
                ('preferred_contact_method', models.CharField(choices=[('email', 'Email'), ('phone', 'Phone')], default='email', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='mainapp.client')),
                ('client_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='managed_properties', to='mainapp.clientmanagers')),
            ],
        ),
    ]
