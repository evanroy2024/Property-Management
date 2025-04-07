from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Client(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    PREFERRED_CONTACT_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]
    preferred_contact_method = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, default='email'
    )

    # Contact Person 1
    contact1_name = models.CharField(max_length=150, blank=True, null=True)
    contact1_email = models.EmailField(blank=True, null=True)
    contact1_phone = models.CharField(max_length=15, blank=True, null=True)
    contact1_preferred = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, blank=True, null=True
    )

    # Contact Person 2
    contact2_name = models.CharField(max_length=150, blank=True, null=True)
    contact2_email = models.EmailField(blank=True, null=True)
    contact2_phone = models.CharField(max_length=15, blank=True, null=True)
    contact2_preferred = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, blank=True, null=True
    )

    # Contact Person 3
    contact3_name = models.CharField(max_length=150, blank=True, null=True)
    contact3_email = models.EmailField(blank=True, null=True)
    contact3_phone = models.CharField(max_length=15, blank=True, null=True)
    contact3_preferred = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"



from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class ClientManagers(models.Model):  # Unique name to avoid conflicts
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)

    PREFERRED_CONTACT_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]
    preferred_contact_method = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, default='email'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)  # Hash password before saving

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Verify password

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):  # Avoid double hashing
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Vendor(models.Model):
    SERVICE_CHOICES = [
        ('Appliance Repair', 'Appliance Repair'),
        ('Artificial Turf', 'Artificial Turf'),
        ('AV', 'AV'),
        ('Car Detailer', 'Car Detailer'),
        ('Carpet Cleaning', 'Carpet Cleaning'),
        ('Caterer / Chef', 'Caterer / Chef'),
        ('Countertops', 'Countertops'),
    ]

    company_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES , blank=True, null=True)

    def __str__(self):
        return self.company_name
