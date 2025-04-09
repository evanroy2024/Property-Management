from django.db import models

# Create your models here.
from django.db import models

class SocialLinks(models.Model):
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    pinterest = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Social Links ({self.id})"

from django.db import models

class MailConfiguration(models.Model):
    email_host = models.CharField(max_length=255, blank=True, null=True)
    email_port = models.PositiveIntegerField(blank=True, null=True)
    email_host_user = models.EmailField(blank=True, null=True)
    email_host_password = models.CharField(max_length=255, blank=True, null=True)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    default_from_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Mail Configuration ({self.id})"

from django.db import models

class CallConfiguration(models.Model):
    SERVICE_CHOICES = [
        ('twilio', 'Twilio'),
        ('plivo', 'Plivo'),
        ('nexmo', 'Nexmo'),
        ('custom', 'Custom'),
    ]

    service_provider = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='twilio')
    account_sid = models.CharField(max_length=255, blank=True, null=True)
    auth_token = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, help_text="Registered calling number", blank=True, null=True)
    webhook_url = models.URLField(blank=True, null=True, help_text="URL to receive call events")

    use_voice_call = models.BooleanField(default=True)
    use_sms = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.service_provider.capitalize()} Configuration ({self.phone_number})"
