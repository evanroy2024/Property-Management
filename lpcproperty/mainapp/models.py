from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid
import random
import string

class Client(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=15,blank=True, null=True)
    office_phone = models.CharField(max_length=15, blank=True, null=True)
    business_address = models.CharField(max_length=255, blank=True, null=True)
    PREFERRED_CONTACT_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('text', 'text'),

    ]
    preferred_contact_method = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, default='email'
    )
    PRIORITY_CHOICES = [
    ('primary', 'Primary'),
    ('secondary', 'Secondary'),
    ('tertiary', 'Tertiary'),
    ]
    # Contact Person 1
    contact1_name = models.CharField(max_length=150, blank=True, null=True)
    contact1_last_name = models.CharField(max_length=150, blank=True, null=True)
    contact1_email = models.EmailField(blank=True, null=True)
    contact1_phone = models.CharField(max_length=15, blank=True, null=True)
    contact1_office_phone = models.CharField(max_length=15, blank=True, null=True)
    contact1_buisness_adress = models.CharField(max_length=155, blank=True, null=True)
    contact1_preferred = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, blank=True, null=True
    )
    contact1_priority = models.CharField(
    max_length=10, choices=PRIORITY_CHOICES, blank=True, null=True
    )

    # Contact Person 2
    contact2_name = models.CharField(max_length=150, blank=True, null=True)
    contact2_last_name = models.CharField(max_length=150, blank=True, null=True)
    contact2_email = models.EmailField(blank=True, null=True)
    contact2_phone = models.CharField(max_length=15, blank=True, null=True)
    contact2_office_phone = models.CharField(max_length=15, blank=True, null=True)
    contact2_buisness_adress = models.CharField(max_length=155, blank=True, null=True)
    contact2_preferred = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, blank=True, null=True
    )
    contact2_priority = models.CharField(
    max_length=10, choices=PRIORITY_CHOICES, blank=True, null=True
    )


    # Contact Person 3
    contact3_name = models.CharField(max_length=150, blank=True, null=True)
    contact3_last_name = models.CharField(max_length=150, blank=True, null=True)
    contact3_email = models.EmailField(blank=True, null=True)
    contact3_phone = models.CharField(max_length=15, blank=True, null=True)
    contact3_office_phone = models.CharField(max_length=15, blank=True, null=True)
    contact3_buisness_adress = models.CharField(max_length=155, blank=True, null=True)
    contact3_preferred = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, blank=True, null=True
    )
    contact3_priority = models.CharField(
    max_length=10, choices=PRIORITY_CHOICES, blank=True, null=True
    )
    # Contact Person 3
    contact4_name = models.CharField(max_length=150, blank=True, null=True)
    contact4_last_name = models.CharField(max_length=150, blank=True, null=True)
    contact4_email = models.EmailField(blank=True, null=True)
    contact4_phone = models.CharField(max_length=15, blank=True, null=True)
    contact4_office_phone = models.CharField(max_length=15, blank=True, null=True)
    contact4_buisness_adress = models.CharField(max_length=155, blank=True, null=True)
    contact4_preferred = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, blank=True, null=True
    )
    contact4_priority = models.CharField(
    max_length=10, choices=PRIORITY_CHOICES, blank=True, null=True
    )

    # Contact Person 3
    contact5_name = models.CharField(max_length=150, blank=True, null=True)
    contact5_last_name = models.CharField(max_length=150, blank=True, null=True)
    contact5_email = models.EmailField(blank=True, null=True)
    contact5_phone = models.CharField(max_length=15, blank=True, null=True)
    contact5_office_phone = models.CharField(max_length=15, blank=True, null=True)
    contact5_buisness_adress = models.CharField(max_length=155, blank=True, null=True)
    contact5_preferred = models.CharField(
        max_length=10, choices=PREFERRED_CONTACT_CHOICES, blank=True, null=True
    )
    contact5_priority = models.CharField(
    max_length=10, choices=PRIORITY_CHOICES, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def generate_username(self):
        base = (self.first_name + self.last_name).lower()
        return f"{base}{uuid.uuid4().hex[:6]}"

    def generate_password(self, length=10):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))
    
    def send_credentials_email(self):
        subject = "Welcome to LOTUS PROPERTY MANAGEMENT SYSTEM - Your Login Credentials"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [self.email]

        text_content = f"""
        Welcome to LOTUS PROPERTY MANAGEMENT SYSTEM!

        You can login here: https://backend.lotuspmc.com/login

        Your credentials are:
        Username: {self.username}
        Password: {self._raw_password}

        Please keep this information confidential.
        """

        html_content = f"""
        <html>
        <body>
            <h2>Welcome to LOTUS PROPERTY MANAGEMENT SYSTEM!</h2>
            <p>You can login here: <a href="https://backend.lotuspmc.com/login">Login Page</a></p>
            <p><strong>Your credentials are:</strong></p>
            <ul>
            <li>Username: {self.username}</li>
            <li>Password: {self._raw_password}</li>
            </ul>
            <p>Please keep this information confidential.</p>
        </body>
        </html>
        """

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

    def save(self, *args, **kwargs):
        self._raw_password = None
        username_added = False
        password_added = False

        # Check if this is a new instance
        is_new = self.pk is None

        if is_new:
            # New client - generate username and password
            if not self.username:
                self.username = self.generate_username()
                username_added = True
            
            if not self.password:
                raw_password = self.generate_password()
                self._raw_password = raw_password
                self.password = make_password(raw_password)
                password_added = True
            elif not self.password.startswith('pbkdf2_'):
                self._raw_password = self.password
                self.password = make_password(self.password)
                password_added = True
        else:
            # Existing client - check for changes
            old_instance = Client.objects.get(pk=self.pk)
            
            # Check username change
            if self.username != old_instance.username:
                username_added = True
            
            # Check password change
            if self.password != old_instance.password:
                if not self.password.startswith('pbkdf2_'):
                    self._raw_password = self.password
                    self.password = make_password(self.password)
                else:
                    # Password was already hashed but different - keep it
                    self._raw_password = "Password has been updated"
                password_added = True

        super().save(*args, **kwargs)

        if username_added or password_added:
            self.send_credentials_email()
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
    phone_number = models.CharField(max_length=15,blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    office_phone = models.CharField(max_length=15, null=True, blank=True)
    business_address = models.TextField(null=True, blank=True)
    PREFERRED_CONTACT_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('text', 'text'),
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
    company_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    suite = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    service = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name

class VendorContact(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cell = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.vendor.company_name}"

class VendorServices(models.Model):
    service = models.CharField(max_length=255)

    