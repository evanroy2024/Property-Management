from django.db import models
from mainapp.models import Client, Vendor  # Import from mainapp

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('open', 'Open'),
        ('completed', 'Completed'),
        ('denied', 'Denied'),
    ]
    REQUEST_TYPE_CHOICES = [
        ('interior_residence', 'INTERIOR RESIDENCE'),
        ('exterior_structure', 'EXTERIOR STRUCTURE'),
        ('exterior_grounds', 'EXTERIOR GROUNDS'),
        ('housekeeping', 'HOUSEKEEPING'),
        ('water_features', 'WATER FEATURES'),
        ('storm_preparedness', 'STORM PREPAREDNESS'),
        ('other', 'OTHER'),
    ]
    
    user = models.ForeignKey(Client, on_delete=models.CASCADE)  # Use Client from mainapp
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPE_CHOICES)  # Updated field
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)  # Use Vendor from mainapp
    created_at = models.DateTimeField(auto_now_add=True)
    floor_plan_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.request_type


from django.db import models

class PrearrivalInformation(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    arrival_date = models.DateField(null=True, blank=True)
    arrival_time = models.TimeField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    pool_temperature = models.FloatField(null=True, blank=True)
    hot_bath_temperature = models.FloatField(null=True, blank=True)
    
    INDOOR_LIGHTS_CHOICES = [('all_on', 'All On'), ('all_off', 'All Off')]
    indoor_lights = models.CharField(max_length=10, choices=INDOOR_LIGHTS_CHOICES, null=True, blank=True)
    
    OUTDOOR_LIGHTS_CHOICES = [('all_on', 'All On'), ('all_off', 'All Off')]
    outdoor_lights = models.CharField(max_length=10, choices=OUTDOOR_LIGHTS_CHOICES, null=True, blank=True)
    
    WINDOW_POSITION_CHOICES = [('up', 'Up'), ('down', 'Down'), ('sideway', 'Sideway')]
    window_position = models.CharField(max_length=10, choices=WINDOW_POSITION_CHOICES, null=True, blank=True)
    
    music_genre = models.CharField(max_length=255, null=True, blank=True)
    flower_type = models.CharField(max_length=255, null=True, blank=True)
    flower_location = models.CharField(max_length=255, null=True, blank=True)
    
    groceries_details = models.TextField(null=True, blank=True)
    alcohol = models.TextField(null=True, blank=True)
    housekeeping = models.TextField(null=True, blank=True)
    transportation = models.TextField(null=True, blank=True)
    automobiles = models.TextField(null=True, blank=True)
    additional = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.username if self.user else 'No User'}"


class DepartureInformation(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)

    housekeeping = models.TextField(null=True, blank=True)
    wash = models.TextField(null=True, blank=True)
    trash = models.TextField(null=True, blank=True)
    additional = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.username if self.user else 'No User'}"
    


# ConciergeServiceRequest   Starts here -----------------------------------------------------------

class ConciergeServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('open', 'Open'),
        ('completed', 'Completed'),
        ('denied', 'Denied'),
    ]

    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.status}"

# ConciergeServiceRequest ends here ------------------------------------------------------------------






