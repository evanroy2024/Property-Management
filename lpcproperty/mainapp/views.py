from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
import random
from mainapp.utils import client_login_required
from contentpage.models import Testimonial

from django.contrib.auth.decorators import login_required


# @client_login_required

# Create your views here.
def home(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'mainapp/home.html', {'testimonials': testimonials})

# Ending of login signing here ------------------------------------------------------------------------------------------

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .models import Client ,ClientManagers

def client_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            client = Client.objects.get(username=username)
            if client.check_password(password):
                request.session['client_id'] = client.id  # Store user session
                return redirect('mainapp:dashboard')  # Redirect to start page
            else:
                messages.error(request, "Invalid credentials!")
        except Client.DoesNotExist:
            messages.error(request, "User not found!")

    return render(request, "mainapp/login.html")

@client_login_required
def dashboard(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('mainapp:client_login')

    client = Client.objects.get(id=client_id)
    return render(request, "dashboard/dashboard.html", {"client": client})

def client_logout(request):
    logout(request)  # Clear session
    return redirect('mainapp:client_login')

# Starting of client manager here ----------------------------------------------------------------------------------------------
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class ClientManager(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store hashed passwords
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

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

# Ending of login signing here ------------------------------------------------------------------------------------------
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from propertydetails.models import PropertyManagement
from .utils import client_login_required  # Import the decorator

from django.shortcuts import render
from .utils import client_login_required  # Import the decorator


@client_login_required
def client_properties(request):
    client_id = request.session['client_id']  # Since decorator ensures login, we can directly access this
    client = Client.objects.get(id=client_id)  # Get the client instance
    properties = PropertyManagement.objects.filter(client=client)  # Get only this client's properties

    # Contact persons
    contacts = [
        {"name": client.contact1_name, "email": client.contact1_email, "phone": client.contact1_phone, "preferred": client.contact1_preferred},
        {"name": client.contact2_name, "email": client.contact2_email, "phone": client.contact2_phone, "preferred": client.contact2_preferred},
        {"name": client.contact3_name, "email": client.contact3_email, "phone": client.contact3_phone, "preferred": client.contact3_preferred},
    ]

    # Filter out empty contacts (if they are not added)
    contacts = [c for c in contacts if c["name"]]

    return render(request, 'property/properties.html', {'properties': properties, 'contacts': contacts})

from django.shortcuts import render, redirect
from django.contrib import messages
from servicedetails.models import ServiceRequest
from mainapp.models import Client  # Ensure Client is imported


from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import Client
from servicedetails.models import ServiceRequest

def service_request(request):
    if request.method == "POST":
        client_id = request.session.get("client_id")  # Get client ID from session

        if not client_id:
            messages.error(request, "You must be logged in to submit a request.")
            return redirect("mainapp:client_login")  # Redirect to login page

        try:
            client = Client.objects.get(id=client_id)  # Fetch Client instance
        except Client.DoesNotExist:
            messages.error(request, "Client does not exist.")
            return redirect("mainapp:dashboard")

        request_type = request.POST.get("request_type")
        description = request.POST.get("description")

        if not request_type or not description:
            messages.error(request, "All fields are required!")
            return redirect("mainapp:service_request")

        # Create and save the service request
        ServiceRequest.objects.create(
            user=client, 
            request_type=request_type,
            description=description
        )

        messages.success(request, "Service request submitted successfully!")
        return redirect("mainapp:dashboard")

    return render(request, "services/service.html", {"request_types": ServiceRequest.REQUEST_TYPE_CHOICES})


def docoments(request):
    return render(request, 'mainapp/documents.html')

def pre_arrival(request):
    return render(request, 'services/pre_arrival.html')

def departure(request):
    return render(request, 'services/departure.html')


# All services go there Start ----------------------------------------------------------------------------------
def open_services(request):
    # Get the logged-in client from the session
    client_id = request.session.get("client_id")

    if not client_id:
        return redirect("mainapp:client_login")  # Redirect if not logged in

    try:
        client = Client.objects.get(id=client_id)  # Fetch the client instance
    except Client.DoesNotExist:
        return redirect("mainapp:client_login")

    # Fetch only the "open" service requests for the logged-in client
    service_requests = ServiceRequest.objects.filter(user=client, status='open').order_by('-created_at')

    return render(request, 'services/allservices/open_services.html', {'service_requests': service_requests})


def completed_services(request):
    # Get the logged-in client from the session
    client_id = request.session.get("client_id")

    if not client_id:
        return redirect("mainapp:client_login")  # Redirect if not logged in

    try:
        client = Client.objects.get(id=client_id)  # Fetch the client instance
    except Client.DoesNotExist:
        return redirect("mainapp:client_login")

    # Fetch only the "completed" service requests for the logged-in client
    service_requests = ServiceRequest.objects.filter(user=client, status='completed').order_by('-created_at')

    return render(request, 'services/allservices/completed_services.html', {'service_requests': service_requests})

def denied_services(request):
    # Get the logged-in client from the session
    client_id = request.session.get("client_id")

    if not client_id:
        return redirect("mainapp:client_login")  # Redirect if not logged in

    try:
        client = Client.objects.get(id=client_id)  # Fetch the client instance
    except Client.DoesNotExist:
        return redirect("mainapp:client_login")

    # Fetch only the "denied" service requests for the logged-in client
    service_requests = ServiceRequest.objects.filter(user=client, status='denied').order_by('-created_at')

    return render(request, 'services/allservices/denied_services.html', {'service_requests': service_requests})

# All services go there End  ----------------------------------------------------------------------------------

# All concierge go there Start  ----------------------------------------------------------------------------------
from servicedetails.models import ConciergeServiceRequest

def open_concierge_services(request):
    client_id = request.session.get("client_id")

    if not client_id:
        return redirect("mainapp:client_login")

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return redirect("mainapp:client_login")

    service_requests = ConciergeServiceRequest.objects.filter(user=client, status='open').order_by('-created_at')

    return render(request, 'services/concierge/open_services.html', {'service_requests': service_requests})

def completed_concierge_services(request):
    client_id = request.session.get("client_id")

    if not client_id:
        return redirect("mainapp:client_login")

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return redirect("mainapp:client_login")

    service_requests = ConciergeServiceRequest.objects.filter(user=client, status='completed').order_by('-created_at')

    return render(request, 'services/concierge/completed_services.html', {'service_requests': service_requests})

def denied_concierge_services(request):
    client_id = request.session.get("client_id")

    if not client_id:
        return redirect("mainapp:client_login")

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return redirect("mainapp:client_login")

    service_requests = ConciergeServiceRequest.objects.filter(user=client, status='denied').order_by('-created_at')

    return render(request, 'services/concierge/denied_services.html', {'service_requests': service_requests})

# All concierge go there End  ----------------------------------------------------------------------------------

def client_manager_support(request):
    return render(request, 'mainapp/client_manager_support.html')

# def get_started(request):
#     return render(request, 'mainapp/get_started.html')

# def dashboard(request):
#     return render(request, 'dashboard/dashboard.html')

# def testui(request):
#     return render(request, 'ui/1.html')



def manager_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            # Check if user exists by username or email
            user = ClientManagers.objects.get(username=username)  
        except ClientManagers.DoesNotExist:
            try:
                user = ClientManagers.objects.get(email=username)
            except ClientManagers.DoesNotExist:
                messages.error(request, "User not found!")
                return redirect("mainapp:manager_login")  

        # Check password
        if check_password(password, user.password):
            request.session['manager_id'] = user.id  # Store manager ID in session
            request.session['manager_username'] = user.username  # Store username for display

            return redirect("mainapp:manager_home")  # Redirect to manager home
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("mainapp:manager_login")  

    return render(request, "mainapp/manager_login.html")


def manager_home(request):
    manager_id = request.session.get('manager_id')
    manager_username = request.session.get('manager_username')

    if not manager_id:
        return redirect("mainapp:manager_login")  # If not logged in, send back to login

    return render(request, "mainapp/manager_home.html", {"manager_username": manager_username})
