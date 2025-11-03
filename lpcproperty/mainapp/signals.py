# mainapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client, ClientManagers, Vendor, VendorContact
import sys
import os
import re

# Import SMS service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sms_service import SlickTextSMSService


def sync_phone_numbers(instance, phone_fields):
    sms_service = SlickTextSMSService()

    for field in phone_fields:
        phone = getattr(instance, field, None)
        if phone and phone.strip():
            digits_only = re.sub(r'\D', '', phone)
            if len(digits_only) < 10:
                print(f"Skipping invalid phone: {phone} (only {len(digits_only)} digits)")
                continue

            if sms_service.lookup_contact(phone):
                print(f"Contact {phone} already exists, skipping")
                continue

            result = sms_service.create_contact(
                phone_number=phone,
                first_name=getattr(instance, 'first_name', ''),
                last_name=getattr(instance, 'last_name', ''),
                email=getattr(instance, 'email', '')
            )

            if result['success']:
                print(f"Successfully created contact: {phone}")
            else:
                print(f"Failed to create contact {phone}: {result['error']}")


@receiver(post_save, sender=Client)
def sync_client_phones(sender, instance, created, **kwargs):
    sync_phone_numbers(instance, [
        'phone_number',
        'contact1_phone',
        'contact2_phone',
        'contact3_phone',
        'contact4_phone',
        'contact5_phone',
    ])


@receiver(post_save, sender=ClientManagers)
def sync_clientmanager_phones(sender, instance, created, **kwargs):
    sync_phone_numbers(instance, ['phone_number', 'office_phone'])


@receiver(post_save, sender=Vendor)
def sync_vendor_phones(sender, instance, created, **kwargs):
    sync_phone_numbers(instance, ['phone_number'])


@receiver(post_save, sender=VendorContact)
def sync_vendorcontact_phones(sender, instance, created, **kwargs):
    sync_phone_numbers(instance, ['cell'])
