from django.db import models
from mainapp.models import Client, ClientManagers  # Import existing models
from mainapp.models import Vendor  # Import Vendor model from mainapp

class PropertyManagement(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="properties")
    client_manager = models.ForeignKey(ClientManagers, on_delete=models.CASCADE, related_name="managed_properties")

    address = models.CharField(max_length=255)
    size_of_home = models.CharField(max_length=50)
    number_of_stories = models.PositiveIntegerField()
    construction_type = models.CharField(max_length=100)
    year_built = models.PositiveIntegerField()

    has_pool = models.BooleanField(default=False)
    gated_community = models.BooleanField(default=False)
    impact_windows = models.BooleanField(default=False)
    has_hoa = models.BooleanField(default=False)
    gated_property = models.BooleanField(default=False)

    PREFERRED_CONTACT_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]
    preferred_contact_method = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, default='email'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    # Floor Plan Fields (Supports Image & PDF)
    floor_plan_1_name = models.CharField(max_length=100, blank=True, null=True)
    floor_plan_1_file = models.FileField(upload_to="floor_plans/", blank=True, null=True)

    floor_plan_2_name = models.CharField(max_length=100, blank=True, null=True)
    floor_plan_2_file = models.FileField(upload_to="floor_plans/", blank=True, null=True)

    floor_plan_3_name = models.CharField(max_length=100, blank=True, null=True)
    floor_plan_3_file = models.FileField(upload_to="floor_plans/", blank=True, null=True)

    floor_plan_4_name = models.CharField(max_length=100, blank=True, null=True)
    floor_plan_4_file = models.FileField(upload_to="floor_plans/", blank=True, null=True)

    # Add created_at field

    def __str__(self):
        return f"Property at {self.address} - Managed by {self.client_manager}"

class PropertyImprovement(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('open', 'Open'),
        ('completed', 'Completed'),
        ('denied', 'Denied'),
    ]

    CLIENT_APPROVAL_CHOICES = [
        ('pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Deny', 'Deny'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="property_improvements") 
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    pino = models.CharField(max_length=50, unique=True)  
    description = models.TextField()  
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  
    client_approval = models.CharField(max_length=20, choices=CLIENT_APPROVAL_CHOICES, default='pending')  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  



# Chat Details --------------------------------------------------------------------
