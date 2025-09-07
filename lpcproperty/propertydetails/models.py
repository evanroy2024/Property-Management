from django.db import models
from mainapp.models import Client, ClientManagers  # Import existing models
from mainapp.models import Vendor  # Import Vendor model from mainapp

class PropertyManagement(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="properties")
    client_manager = models.ForeignKey(ClientManagers, on_delete=models.CASCADE, related_name="managed_properties")

    address = models.CharField(max_length=255)
    street_line1 = models.CharField(max_length=255, blank=True, null=True)
    street_line2 = models.CharField(max_length=255, blank=True, null=True)

    size_of_home = models.CharField(max_length=50)
    number_of_stories = models.PositiveIntegerField()
    construction_type = models.CharField(max_length=100)
    year_built = models.PositiveIntegerField()

    has_pool = models.BooleanField(default=False)
    gated_community = models.BooleanField(default=False)
    impact_windows = models.BooleanField(default=False)
    has_hoa = models.BooleanField(default=False)
    gated_property = models.BooleanField(default=False)

    basketball_court = models.BooleanField(default=False)
    tennis_court = models.BooleanField(default=False)
    pickleball_court = models.BooleanField(default=False)
    hot_tub = models.BooleanField(default=False)
    outdoor_kitchen_gazebo = models.BooleanField(default=False)
    waterfront = models.BooleanField(default=False)

    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)

    PREFERRED_CONTACT_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]
    preferred_contact_method = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, default='email'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    additional_info = models.TextField(blank=True, null=True)
    # Floor Plan Fields (Supports Image & PDF)
  
    property_pic = models.ImageField(upload_to='property_images/', null=True, blank=True)
    # Add created_at field

    def __str__(self):
        return f"Property at {self.address} - Managed by {self.client_manager}"


class Floor(models.Model):
    property = models.ForeignKey(PropertyManagement, on_delete=models.CASCADE, related_name='floors')
    floor_name = models.CharField(max_length=255)
    floor_imgae = models.ImageField(upload_to='floor_images/', null=True, blank=True)

    def __str__(self):
        return f"Property at {self.floor_name} "

class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    room_name = models.CharField(max_length=255)
    room_size = models.CharField(max_length=255)
    room_image = models.ImageField(upload_to='rooms_images/', null=True, blank=True)

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
