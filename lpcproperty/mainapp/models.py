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
    def send_credentials_email(self):

        subject = "Welcome to LOTUS PROPERTY MANAGEMENT SYSTEM - Your Login Credentials"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [
            email for email in [
                self.email,
                self.contact1_email,
                self.contact2_email,
                self.contact3_email,
                self.contact4_email,
                self.contact5_email
            ] if email
        ]


        text_content = f"""
        Welcome to Lotus Property Management!

        Welcome to the Lotus family — we’re truly glad to have you with us. Our team is fully committed to caring for your property with the attention, dedication, and support you deserve.

        To Get Started:

        1. You have been assigned a temporary Username and Password. These are below.
        Username: {self.username}
        Password: {self._raw_password}

        Please use these temporary credentials to log in to your Lotus dashboard. You may copy and paste them into the entry fields.

        Login Page: https://backend.lotuspmc.com/login

        2. After logging in, you’ll be redirected to the dashboard.

        3. Navigate to "Profile & Security" (lavender colored box near the bottom of the page) and select it.

        4. The Update Profile page will appear. Please update your Username and Password.

        5. Click Update on the bottom left of the page to apply the changes.

        6. After selecting Update, a new screen will appear confirming your credentials have been successfully updated.
        PLEASE REMEMBER TO SAVE YOUR LOG-IN CREDENTIALS.

        7. Use your new credentials for all future logins.

        Well, there you have it — you are all set to go! If you have any questions regarding setup or need assistance with the site, please do not hesitate to let us know. We thank you for your business and look forward to taking care of your property.

        Sincerely,

        Sean Couch, Co-Founder
        sean@lotuspmc.com
        336.918.3632

        Neal Jones, Co-Founder
        neal@lotuspmc.com
        415.524.3120

        This is an automated message. Replies to this email are not monitored.
        """
        html_content = f"""
<html>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f6; padding: 20px;">

  <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); overflow: hidden;">

    <!-- Top Header -->
    <div style="background:#1f3c88; padding:22px 28px;">
      <img src="https://backend.lotuspmc.com/static/logo.png"
           alt="Lotus Property Management"
           style="height:54px; display:block;">
    </div>

    <!-- Content -->
    <div style="padding:28px;">

      <h2 style="color:#2b4b80; margin-top:0;">
        Welcome to Lotus Property Management!
      </h2>

      <p style="font-size:15px; color:#333;">
        Welcome to the Lotus family — we’re truly glad to have you with us. Our team is fully committed to caring for your property with the attention, dedication, and support you deserve.
      </p>

      <h3 style="color:#2b4b80;">To Get Started</h3>

      <p style="font-size:14px; color:#333;">
        You have been assigned a temporary Username and Password:
      </p>

      <div style="background:#f8f9fb; padding:16px; border-radius:8px; margin-bottom:16px;">
        <p style="margin:6px 0;"><strong>Username:</strong> {self.username}</p>
        <p style="margin:6px 0;"><strong>Password:</strong> {self._raw_password}</p>
      </div>

      <p style="font-size:14px; color:#333;">
        Please use these temporary credentials to log in to your Lotus dashboard. You may copy and paste them into the entry fields.
      </p>

      <p style="text-align:center; margin:22px 0;">
        <a href="https://backend.lotuspmc.com/login"
           style="background:#2b4b80; color:#ffffff; padding:12px 24px; border-radius:8px; text-decoration:none; font-weight:bold;">
          Go to Login Page
        </a>
      </p>

      <ol style="padding-left:20px; font-size:14px; color:#333;">
        <li>After logging in, you’ll be redirected to the dashboard.</li>
        <li>Navigate to <strong>Profile & Security</strong> (lavender colored box near the bottom of the page).</li>
        <li>The Update Profile page will appear. Update your <strong>Username</strong> and <strong>Password</strong>.</li>
        <li>Click <strong>Update</strong> on the bottom left to apply the changes.</li>
        <li>A confirmation screen will appear once your credentials are updated.</li>
        <li><strong>Please remember to save your log-in credentials.</strong></li>
        <li>Use your new credentials for all future logins.</li>
      </ol>

      <p style="font-size:14px; color:#333; margin-top:18px;">
        You are all set to go! If you have any questions regarding setup or need assistance with the site, please do not hesitate to let us know. We thank you for your business and look forward to taking care of your property.
      </p>

      <hr style="margin:26px 0; border:none; border-top:1px solid #e6e6e6;">

      <p style="font-size:14px; color:#333;">
        <strong>Sean Couch</strong>, Co-Founder<br>
        <a href="mailto:sean@lotuspmc.com" style="color:#2b4b80; text-decoration:none;">sean@lotuspmc.com</a><br>
        336.918.3632
      </p>

      <p style="font-size:14px; color:#333;">
        <strong>Neal Jones</strong>, Co-Founder<br>
        <a href="mailto:neal@lotuspmc.com" style="color:#2b4b80; text-decoration:none;">neal@lotuspmc.com</a><br>
        415.524.3120
      </p>

      <p style="font-size:12px; color:#777; margin-top:22px;">
        This is an automated message. Replies to this email are not monitored.
      </p>

    </div>
  </div>

</body>
</html>
"""

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)


    def generate_password(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
        
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

    def generate_username(self):
        import uuid
        base = (self.first_name + self.last_name).lower()
        return f"{base}{uuid.uuid4().hex[:6]}"

    def generate_password(self):
        import random, string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def send_credentials_email(self):
        from django.core.mail import EmailMultiAlternatives
        from django.conf import settings

        subject = "Welcome to LOTUS PROPERTY MANAGEMENT SYSTEM - Your Login Credentials"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [self.email]

        text_content = f"""
        Welcome to LOTUS PROPERTY MANAGEMENT SYSTEM!

        You can login here: https://backend.lotuspmc.com/login

        Your credentials are:
        Username: {self.username}
        Password: {self._raw_password}
        """

        html_content = f"""
        <html><body>
            <h2>Welcome to Lotus Property Management</h2>
            <p>You can login here: <a href="https://backend.lotuspmc.com/login">Login Page</a></p>
            <ul>
                <li>Username: {self.username}</li>
                <li>Password: {self._raw_password}</li>
            </ul>
            <p>Please change your password after login.</p>

             <h3 style="color: #2b4b80;">How to Change Your Username and Password</h3>
                <ol style="padding-left: 20px; color: #333;">
                    <li>Go to the <a href="https://backend.lotuspmc.com/login" style="color: #2b4b80;">Login Page</a> and enter your temporary credentials.</li>
                    <li>After logging in, you’ll be redirected to the dashboard.</li>
                    <li>Navigate to <strong>Profile & Security</strong>.</li>
                    <li>Update your <strong>Username</strong>, <strong>Email</strong>, and/or <strong>Password</strong>.</li>
                    <li>Click <strong>Save</strong> to apply the changes.</li>
                    <li>Use your new credentials for all future logins.</li>
                </ol>
        </body></html>
        """

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

    def save(self, *args, **kwargs):
        self._raw_password = None
        username_added = False
        password_added = False
        is_new = self.pk is None

        if is_new:
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
            old_instance = ClientManagers.objects.get(pk=self.pk)
            if self.username != old_instance.username:
                username_added = True
            if self.password != old_instance.password:
                if not self.password.startswith('pbkdf2_'):
                    self._raw_password = self.password
                    self.password = make_password(self.password)
                password_added = True

        super().save(*args, **kwargs)

        if username_added or password_added:
            self.send_credentials_email()



    
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

    