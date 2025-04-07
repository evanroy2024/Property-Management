from django.db import models

# Create your models here.
from propertydetails.models import PropertyManagement
from mainapp.models import Client, ClientManagers

class Message(models.Model):
    SENDER_TYPE_CHOICES = [
        ('client', 'Client'),
        ('manager', 'Client Manager'),
    ]

    property = models.ForeignKey(PropertyManagement, on_delete=models.CASCADE, related_name='messages')
    sender_type = models.CharField(max_length=10, choices=SENDER_TYPE_CHOICES)
    sender_client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    sender_manager = models.ForeignKey(ClientManagers, on_delete=models.CASCADE, null=True, blank=True)

    message_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def get_sender_display(self):
        if self.sender_type == 'client' and self.sender_client:
            return f"{self.sender_client.username}"
        elif self.sender_type == 'manager' and self.sender_manager:
            return f"{self.sender_manager.username}"
        return "Unknown"

    def __str__(self):
        return f"{self.get_sender_display()} - {self.message_text[:30]}"