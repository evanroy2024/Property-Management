# mainapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Client
import sys
import os
import re

# Import SMS service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sms_service import SlickTextSMSService

@receiver(post_save, sender=Client)
def sync_phones_to_slicktext(sender, instance, created, **kwargs):
    sms_service = SlickTextSMSService()
    
    # Check these 6 phone fields
    phones = [
        instance.phone_number,
        instance.contact1_phone,
        instance.contact2_phone, 
        instance.contact3_phone,
        instance.contact4_phone,
        instance.contact5_phone
    ]
    
    for phone in phones:
        if phone and phone.strip():
            # Skip invalid phone numbers (less than 10 digits)
            digits_only = re.sub(r'\D', '', phone)
            if len(digits_only) < 10:
                print(f"Skipping invalid phone: {phone} (only {len(digits_only)} digits)")
                continue
            
            # Check if contact already exists first
            if sms_service.lookup_contact(phone):
                print(f"Contact {phone} already exists, skipping")
                continue
            
            # Create new contact
            result = sms_service.create_contact(
                phone_number=phone,
                first_name=instance.first_name,
                last_name=instance.last_name,
                email=instance.email
            )
            
            if result['success']:
                print(f"Successfully created contact: {phone}")
            else:
                print(f"Failed to create contact {phone}: {result['error']}")
