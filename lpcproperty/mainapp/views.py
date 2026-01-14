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

# Create your views here.
def home(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'mainapp/home.html', {'testimonials': testimonials})

def learn_more1(request):
    return render(request, 'mainapp/learn_more1.html')

def learn_more2(request):
    return render(request, 'mainapp/learn_more2.html')


def learn_more3(request):
    return render(request, 'mainapp/learn_more3.html')

def process(request):
    return render(request, 'mainapp/process.html')

def get_contact(request):
    return render(request, 'mainapp/contact.html')


# Ending of login signing here ------------------------------------------------------------------------------------------

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .models import Client ,ClientManagers

from mainapp.models import Client, ClientManagers
from django.contrib.auth import authenticate, login as django_login
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import check_password

@csrf_exempt
def client_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 1. Admin check (Django default users)
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            django_login(request, user)
            return redirect('adminmanager:admin_dashboard')

        # 2. Client Manager check
        try:
            manager = ClientManagers.objects.get(username=username)
            if check_password(password, manager.password):  # ✅ fixed
                request.session.flush()
                request.session['manager_id'] = manager.id
                return redirect('clientmanager:admin_dashboard')
        except ClientManagers.DoesNotExist:
            pass

        # 3. Client check
        try:
            client = Client.objects.get(username=username)
            if check_password(password, client.password):  # ✅ fixed
                request.session.flush()
                request.session['client_id'] = client.id
                return redirect('mainapp:dashboard')
        except Client.DoesNotExist:
            pass

        # If all checks fail
        messages.error(request, "Invalid credentials or user type not found.", extra_tags='login_error')

    return render(request, "mainapp/login.html")

def client_profile_update(request):
    client_id = request.session.get("client_id")
    if not client_id:
        return redirect("mainapp:login")

    client = Client.objects.get(id=client_id)

    if request.method == "POST":
        new_username = request.POST.get("username")
        new_email = request.POST.get("email")
        new_password = request.POST.get("password")

        # username unique check only inside Client model
        if Client.objects.exclude(id=client.id).filter(username=new_username).exists():
            messages.error(request, "Username already taken.")
            return redirect("mainapp:client_profile_update")

        client.username = new_username
        client.email = new_email

        if new_password:
            client.password = make_password(new_password)

        client.save()
        messages.success(request, "Updated successfully.")
        return redirect("mainapp:client_profile_update")

    return render(request, "mainapp/client_profile_update.html", {"client": client})


def profile_update(request):
    client_id = request.session.get("client_id")
    if not client_id:
        return redirect("mainapp:login")

    client = Client.objects.get(id=client_id)

    return render(
        request,
        "mainapp/client_profile_confirm.html",
        {"client": client}
    )

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from .models import Client, ClientManagers

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from .models import Client, ClientManagers
import random

otp_storage = {}  # Temporary in-memory OTP storage


class ClientPasswordChangeRequestView(View):
    template_name = "mainapp/request_password_change.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")

        # check if email belongs to client or manager
        user = None
        user_type = None
        try:
            user = Client.objects.get(email=email)
            user_type = "client"
        except Client.DoesNotExist:
            try:
                user = ClientManagers.objects.get(email=email)
                user_type = "manager"
            except ClientManagers.DoesNotExist:
                user = None

        if user:
            otp = str(random.randint(100000, 999999))
            otp_storage[email] = {"otp": otp, "type": user_type}

            send_mail(
                    "Your OTP for Password Change",
                    f"Your OTP is {otp}",
                    "lotusonboard@sbnai.net",  # ✅ Must match EMAIL_HOST_USER
                    [email],
                )
            messages.success(request, "OTP sent to your email.")
            return redirect("mainapp:client_password_verify")
        else:
            messages.error(request, "No user found with this email.")
            return render(request, self.template_name)
        

class ClientPasswordVerifyView(View):
    template_name = "mainapp/verify_otp.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")

        if email in otp_storage and otp_storage[email]["otp"] == otp:
            user_type = otp_storage[email]["type"]

            if user_type == "client":
                user = Client.objects.get(email=email)
            else:
                user = ClientManagers.objects.get(email=email)

            user.password = make_password(new_password)
            user.save()

            del otp_storage[email]
            messages.success(request, "Password changed successfully.")
            return redirect("mainapp:client_login")  # update with your login view name
        else:
            messages.error(request, "Invalid OTP.")
            return render(request, self.template_name)


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

from propertydetails.models import PropertyManagement   

# def client_properties(request):
#     client_id = request.session['client_id']
#     client = Client.objects.get(id=client_id)

#     properties = PropertyManagement.objects.filter(
#         client=client
#     ).prefetch_related('floors__rooms', 'client_manager')

#     if not properties.exists():
#         return render(request, 'property/properties.html', {
#             'properties': [],
#         })

#     # selected property
#     selected_property_id = request.GET.get('property')
#     if selected_property_id:
#         selected_property = properties.filter(id=selected_property_id).first()
#     else:
#         selected_property = properties.first()

#     contacts = [
#         {"name": f"{client.contact1_last_name}, {client.contact1_name}", "email": client.contact1_email, "phone": client.contact1_phone, "preferred": client.contact1_preferred},
#         {"name": f"{client.contact2_last_name}, {client.contact2_name}", "email": client.contact2_email, "phone": client.contact2_phone, "preferred": client.contact2_preferred},
#         {"name": f"{client.contact3_last_name}, {client.contact3_name}", "email": client.contact3_email, "phone": client.contact3_phone, "preferred": client.contact3_preferred},
#     ]
#     contacts = [c for c in contacts if c["name"]]

#     return render(request, 'property/properties.html', {
#         'properties': properties,                 # for dropdown
#         'property': selected_property,             # SINGLE property
#         'contacts': contacts,
#         'client_manager': selected_property.client_manager if selected_property else None,
#     })


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
def build_email(title, rows_html, button_text):
    return f"""
    <div style="background:#eef2f7;padding:40px 0;font-family:Roboto,Arial,Helvetica,sans-serif;">
      <div style="
          max-width:640px;
          margin:0 auto;
          background:#ffffff;
          border-radius:14px;
          box-shadow:0 10px 25px rgba(0,0,0,0.08);
          overflow:hidden;
      ">

        <!-- HEADER -->
        <div style="
            background:#1e3a8a;
            padding:30px 40px;
            color:#ffffff;
            display:flex;
            align-items:flex-start;
        ">
          <img src="https://backend.lotuspmc.com/static/logo.png"
               alt="Logo"
               style="height:60px;">

          <div style="
              font-size:16px;
              font-weight:500;
              margin-top:17px;
              margin-left:85px;
          ">
            Thank you for contacting us
          </div>
        </div>

        <!-- TITLE -->
        <div style="padding:28px 40px 10px 40px;">
          <div style="
              background:#1e3a8a;
              color:#ffffff;
              padding:20px 26px;
              border-radius:8px;
              font-size:18px;
              font-weight:600;
          ">
            Property Edit Requst 
          </div>
        </div>

        <!-- CONTENT -->
        <div style="padding:24px 40px;color:#1f2937;">
          <table style="width:100%;border-collapse:collapse;">
            {rows_html}
          </table>

          <div style="text-align:center;margin-top:36px;">
            <a href="https://backend.lotuspmc.com/login/"
               style="
                 display:inline-block;
                 background:#cfe9f6;
                 color:#000000;
                 text-decoration:none;
                 padding:16px 38px;
                 border-radius:8px;
                 font-weight:600;
                 font-size:14px;
               ">
              {button_text}
            </a>
          </div>
        </div>

        <!-- FOOTER -->
        <div style="background:#f1f5f9;padding:18px 40px;font-size:12px;color:#64748b;">
          Our team will review this request and take action as required.
          <br>
          This is an automated notification. Please do not reply.
        </div>

      </div>
    </div>
    """
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib import messages

def client_properties(request):
    client_id = request.session['client_id']
    client = Client.objects.get(id=client_id)

    properties = PropertyManagement.objects.filter(
        client=client
    ).prefetch_related('floors__rooms', 'client_manager')

    if not properties.exists():
        return render(request, 'property/properties.html', {
            'properties': [],
        })

    selected_property_id = request.GET.get('property')
    if selected_property_id:
        selected_property = properties.filter(id=selected_property_id).first()
    else:
        selected_property = properties.first()

    # ==============================
    # HANDLE REQUEST EDIT EMAIL
    # ==============================
    if request.method == "POST" and request.POST.get("edit_message"):
        message = request.POST.get("edit_message")
        manager = selected_property.client_manager

        # Build table rows
        rows_html = f"""
        <tr>
          <td style="padding:10px 0;font-weight:600;">Client Name</td>
          <td style="padding:10px 0;">{client.last_name}, {client.first_name}</td>
        </tr>
        <tr>
          <td style="padding:10px 0;font-weight:600;">Property</td>
          <td style="padding:10px 0;">{selected_property.address}</td>
        </tr>
        <tr>
          <td style="padding:10px 0;font-weight:600;">Request</td>
          <td style="padding:10px 0;">{message}</td>
        </tr>
        """

        html_content = build_email(
            title="Property / Client Requested Edit",
            rows_html=rows_html,
            button_text="View Property"
        )

        email = EmailMultiAlternatives(
            subject="Property / Client Requested Edit",
            body=message,  # fallback plain text
            from_email=None,  # DEFAULT_FROM_EMAIL
            to=[manager.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        messages.success(request, "Edit request sent successfully.")
        return redirect(request.path)

    # ==============================
    # CONTACTS
    # ==============================
    contacts = [
        {"name": f"{client.contact1_last_name}, {client.contact1_name}", "email": client.contact1_email, "phone": client.contact1_phone, "preferred": client.contact1_preferred},
        {"name": f"{client.contact2_last_name}, {client.contact2_name}", "email": client.contact2_email, "phone": client.contact2_phone, "preferred": client.contact2_preferred},
        {"name": f"{client.contact3_last_name}, {client.contact3_name}", "email": client.contact3_email, "phone": client.contact3_phone, "preferred": client.contact3_preferred},
    ]
    contacts = [c for c in contacts if c["name"]]

    return render(request, 'property/properties.html', {
        'properties': properties,
        'property': selected_property,
        'contacts': contacts,
        'client_manager': selected_property.client_manager,
    })


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
        client_id = request.session.get("client_id")
        if not client_id:
            messages.error(request, "You must be logged in to submit a request.")
            return redirect("mainapp:client_login")

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            messages.error(request, "Client does not exist.")
            return redirect("mainapp:dashboard")

        request_type = request.POST.get("request_type")
        description = request.POST.get("description")
        floor_plan_name = request.POST.get("floor-plan-selection")  # new optional field

        if not request_type or not description:
            messages.error(request, "All fields are required!")
            return redirect("mainapp:service_request")

        # Create and save the service request
        ServiceRequest.objects.create(
            user=client,
            request_type=request_type,
            description=description,
            floor_plan_name=floor_plan_name  # Save it if present
        )

        messages.success(request, "Service request submitted successfully!" ,)
        return redirect("servicesapp:request_form_success")
    
    client_id = request.session['client_id']
    client = Client.objects.get(id=client_id)
    properties = PropertyManagement.objects.filter(client=client).prefetch_related('floors__rooms')


    return render(request, "services/service.html", {
        "request_types": ServiceRequest.REQUEST_TYPE_CHOICES,
        "properties": properties
    })


def docoments(request):
    return render(request, 'mainapp/documents.html')

@client_login_required
def pre_arrival(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('mainapp:client_login')

    client = Client.objects.get(id=client_id)
    return render(request, "dashboard/dashboard.html", {"client": client})
    
def departure(request):
    return render(request, 'services/departure.html')


# All services go there Start ----------------------------------------------------------------------------------



def open_services(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('mainapp:client_login')

    requests = ServiceRequest.objects.filter(
        user_id=client_id
    ).exclude(
        Q(status='completed', client_approval='Approved') |
        Q(status='denied', client_approval='Denied')
    )

    return render(request, 'services/allservices/open_services.html', {
        'requests': requests
    })
def completed_services(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('mainapp:client_login')

    requests = ServiceRequest.objects.filter(
        user_id=client_id,
        status='completed',
        client_approval='Approved'
    )

    return render(request, 'services/allservices/completed_services.html', {
        'requests': requests
    })


def denied_services(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('mainapp:client_login')

    requests = ServiceRequest.objects.filter(
        user_id=client_id,
        status='denied',
        client_approval='Denied'
    )

    return render(request, 'services/allservices/denied_services.html', {
        'requests': requests
    })


# All services go there End  ----------------------------------------------------------------------------------

# All concierge go there Start  ----------------------------------------------------------------------------------
from servicedetails.models import ConciergeServiceRequest

# def open_concierge_services(request):
#     client_id = request.session.get("client_id")

#     if not client_id:
#         return redirect("mainapp:client_login")

#     try:
#         client = Client.objects.get(id=client_id)
#     except Client.DoesNotExist:
#         return redirect("mainapp:client_login")

#     # Base queryset
#     service_requests = ConciergeServiceRequest.objects.filter(user=client, status='open')

#     # Get filter parameters
#     month_filter = request.GET.get('month')
#     date_filter = request.GET.get('date')

#     # Apply month filter
#     if month_filter:
#         try:
#             month_date = datetime.strptime(month_filter, '%B %Y')
#             service_requests = service_requests.filter(
#                 created_at__year=month_date.year,
#                 created_at__month=month_date.month
#             )
#         except ValueError:
#             pass

#     # Apply date filter
#     if date_filter:
#         try:
#             date_obj = datetime.strptime(date_filter, '%b %d, %Y')
#             service_requests = service_requests.filter(created_at__date=date_obj.date())
#         except ValueError:
#             pass

#     # Order by most recent
#     service_requests = service_requests.order_by('-created_at')

#     # Get unique months for filter dropdown
#     all_requests = ConciergeServiceRequest.objects.filter(user=client, status='open')
#     months = all_requests.dates('created_at', 'month', order='DESC')
#     months_list = [date.strftime('%B %Y') for date in months]

#     # Get unique dates for filter dropdown
#     dates = all_requests.dates('created_at', 'day', order='DESC')
#     dates_list = [date.strftime('%b %d, %Y') for date in dates]

#     return render(request, 'services/concierge/open_services.html', {
#         'service_requests': service_requests,
#         'months': months_list,
#         'dates': dates_list,
#     })


# def completed_concierge_services(request):
#     client_id = request.session.get("client_id")

#     if not client_id:
#         return redirect("mainapp:client_login")

#     try:
#         client = Client.objects.get(id=client_id)
#     except Client.DoesNotExist:
#         return redirect("mainapp:client_login")

#     # Base queryset
#     service_requests = ConciergeServiceRequest.objects.filter(user=client, status='completed')

#     # Get filter parameters
#     month_filter = request.GET.get('month')
#     date_filter = request.GET.get('date')

#     # Apply month filter
#     if month_filter:
#         try:
#             month_date = datetime.strptime(month_filter, '%B %Y')
#             service_requests = service_requests.filter(
#                 created_at__year=month_date.year,
#                 created_at__month=month_date.month
#             )
#         except ValueError:
#             pass

#     # Apply date filter
#     if date_filter:
#         try:
#             date_obj = datetime.strptime(date_filter, '%b %d, %Y')
#             service_requests = service_requests.filter(created_at__date=date_obj.date())
#         except ValueError:
#             pass

#     # Order by most recent
#     service_requests = service_requests.order_by('-created_at')

#     # Get unique months for filter dropdown
#     all_requests = ConciergeServiceRequest.objects.filter(user=client, status='completed')
#     months = all_requests.dates('created_at', 'month', order='DESC')
#     months_list = [date.strftime('%B %Y') for date in months]

#     # Get unique dates for filter dropdown
#     dates = all_requests.dates('created_at', 'day', order='DESC')
#     dates_list = [date.strftime('%b %d, %Y') for date in dates]

#     return render(request, 'services/concierge/completed_services.html', {
#         'service_requests': service_requests,
#         'months': months_list,
#         'dates': dates_list,
#     })


# def denied_concierge_services(request):
#     client_id = request.session.get("client_id")

#     if not client_id:
#         return redirect("mainapp:client_login")

#     try:
#         client = Client.objects.get(id=client_id)
#     except Client.DoesNotExist:
#         return redirect("mainapp:client_login")

#     # Base queryset
#     service_requests = ConciergeServiceRequest.objects.filter(user=client, status='denied')

#     # Get filter parameters
#     month_filter = request.GET.get('month')
#     date_filter = request.GET.get('date')

#     # Apply month filter
#     if month_filter:
#         try:
#             month_date = datetime.strptime(month_filter, '%B %Y')
#             service_requests = service_requests.filter(
#                 created_at__year=month_date.year,
#                 created_at__month=month_date.month
#             )
#         except ValueError:
#             pass

#     # Apply date filter
#     if date_filter:
#         try:
#             date_obj = datetime.strptime(date_filter, '%b %d, %Y')
#             service_requests = service_requests.filter(created_at__date=date_obj.date())
#         except ValueError:
#             pass

#     # Order by most recent
#     service_requests = service_requests.order_by('-created_at')

#     # Get unique months for filter dropdown
#     all_requests = ConciergeServiceRequest.objects.filter(user=client, status='denied')
#     months = all_requests.dates('created_at', 'month', order='DESC')
#     months_list = [date.strftime('%B %Y') for date in months]

#     # Get unique dates for filter dropdown
#     dates = all_requests.dates('created_at', 'day', order='DESC')
#     dates_list = [date.strftime('%b %d, %Y') for date in dates]

#     return render(request, 'services/concierge/denied_services.html', {
#         'service_requests': service_requests,
#         'months': months_list,
#         'dates': dates_list,
#     })

def open_concierge_services(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('mainapp:client_login')

    requests = ConciergeServiceRequest.objects.filter(
        user_id=client_id
    ).exclude(
        Q(status='completed', client_approval='Approved') |
        Q(status='denied', client_approval='Denied')
    )

    return render(request, 'services/concierge/open_services.html', {
        'requests': requests
    })


def completed_concierge_services(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('mainapp:client_login')

    requests = ConciergeServiceRequest.objects.filter(
        user_id=client_id,
        status='completed',
        client_approval='Approved'
    )

    return render(request, 'services/concierge/completed_services.html', {
        'requests': requests
    })


def denied_concierge_services(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('mainapp:client_login')

    requests = ConciergeServiceRequest.objects.filter(
        user_id=client_id,
        status='denied',
        client_approval='Denied'
    )

    return render(request, 'services/concierge/denied_services.html', {
        'requests': requests
    })








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



# All walkthroug report of clients  ------------------------------------------------------------
from django.shortcuts import render

# Create your views here.
# views.py

from django.shortcuts import render
from walkthroughreport.models import WalkthroughReport
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from mainapp.models import Client
CATEGORY_LABELS = {
    "GIE": "General Items - Exterior",
    "GII": "General Items - Interior",
    "GARAGE": "Garage",
    "LAUNDRY": "Laundry / Mudroom",
    "KITCHEN": "Kitchen",
    "BUTLERS": "Butlers",
    "BREAKFAST_AREA": "Breakfast Area",
    "ENTRY_FOYER": "Entry / Foyer",
    "GREAT_ROOM": "Great Room / Family Room",
    "DINING_ROOM": "Dining Room / Area",
    "CLOSETS_MAIN_LEVEL": "Closets - Main Level",
    "CLOSETS_UPPER_LEVEL": "Closets - Upper Level",
    "HALLWAYS_MAIN_LEVEL": "Hallways - Main Level",
    "HALLWAYS_UPPER_LEVEL": "Hallways - Upper Level",
    "BEDROOM1": "Bedroom 1 (Master Bedroom)",
    "BEDROOM2": "Bedroom 2",
    "BEDROOM3": "Bedroom 3",
    "BEDROOM4": "Bedroom 4",
    "BATHROOM1": "Bathroom 1 (Master Bath)",
    "BATHROOM2": "Bathroom 2",
    "BATHROOM3": "Bathroom 3",
    "BATHROOM4": "Bathroom 4",
    "BATHROOM5": "Bathroom 5",
    "GYM": "Gym",
    "THEATRE_MUSIC_ROOM": "Theatre / Music Room",
    "GUEST_HOUSE_SLEEPING_LIVING": "Guest House - Sleeping / Living",
    "GUEST_HOUSE_BATHROOM": "Guest House - Bathroom",
}

def my_reports_view(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('client_login')  # optional: in case someone accesses directly

    reports = WalkthroughReport.objects.filter(user_id=client_id)
    return render(request, 'mainapp/walktrug/my_reports.html', {'reports': reports})

from django.shortcuts import render
from django.http import HttpResponse
from walkthroughreport.models import WalkthroughReport
from django.utils.text import slugify
import csv
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from django.http import HttpResponse, Http404
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import inch


MCQ_CHOICES = [
    ("N/A", "N/A"),
    ("Compliant", "Compliant"),
    ("Heads-Up", "Heads-Up"),
    ("Non-Compliant", "Non-Compliant"),
]
def get_verbose_data(report):
    data = []
    for field in report._meta.fields:
        name = field.name
        if name[-1:].isdigit() and not name.endswith('_remarks'):
            answer = getattr(report, name)
            remark = getattr(report, f"{name}_remarks", '')

            if answer:
                verbose = field.verbose_name or name.replace('_', ' ').capitalize()
                prefix = ''.join(filter(str.isalpha, name)).upper()  # extract 'GIE' from 'gie1'
                data.append((verbose, answer, remark, prefix))
    return data


def export_pdf(request, report_id):
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import TableStyle

    report = WalkthroughReport.objects.get(pk=report_id)
    data = get_verbose_data(report)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=walkthrough_report_{report_id}.pdf'

    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        leftMargin=30,
        rightMargin=30,
        topMargin=50,
        bottomMargin=30
    )

    elements = []
    styles = getSampleStyleSheet()

    # Title with green color
    styles.add(ParagraphStyle(
        name='GreenTitle',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#2e7d32"),
        fontName="Helvetica-Bold",
        alignment=1,  # Center
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontSize=13,
        leading=16,
        spaceAfter=10,
        textColor=colors.HexColor("#003366"),
        fontName="Helvetica-Bold"
    ))

    # Top Title
    elements.append(Paragraph("🏠 Walkthrough Report", styles['GreenTitle']))

    # Underline
    elements.append(Table([[""]], colWidths=[6.3 * inch], style=[
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor("#2e7d32")),
    ]))

    elements.append(Spacer(1, 12))

    # Grouping data by category
    grouped = {}
    for question, answer, remark, category in data:
        if category not in grouped:
            grouped[category] = []
        grouped[category].append((question, answer, remark))

    for category_code, rows in grouped.items():
        label = CATEGORY_LABELS.get(category_code, category_code)

        elements.append(Spacer(1, 14))
        elements.append(Paragraph(f"📌 {label}", styles['SectionTitle']))
        elements.append(Spacer(1, 4))

        table_data = [["Question", "N/A", "Compliant", "Heads-Up", "Non-Compliant", "Remarks"]]

        for i, (question, answer, remark) in enumerate(rows):
            row = [question]
            for choice, _ in MCQ_CHOICES:
                row.append("✔" if answer == choice else "")
            row.append(remark or "-")
            table_data.append(row)

        table = Table(table_data, colWidths=[
            2.3 * inch, 0.7 * inch, 0.8 * inch, 0.9 * inch, 0.9 * inch, 2 * inch
        ])

        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#d9eaf7")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#003366")),
            ('ALIGN', (1, 1), (-2, -1), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ])

        for i in range(1, len(table_data)):
            bg = colors.whitesmoke if i % 2 == 0 else colors.white
            style.add('BACKGROUND', (0, i), (-1, i), bg)

        table.setStyle(style)
        elements.append(table)

    doc.build(elements)
    return response

from django.http import HttpResponse
from openpyxl import Workbook
from walkthroughreport.models import WalkthroughReport
from walkthroughreport.models import CategoryCharField

def export_excel(request, report_id):
    report = WalkthroughReport.objects.get(pk=report_id)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"walkthrough_report_{report_id}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'

    wb = Workbook()
    ws = wb.active
    ws.title = "Walkthrough Report"

    fields = report._meta.get_fields()
    grouped_data = {}

    for field in fields:
        if isinstance(field, CategoryCharField) and getattr(report, field.name):
            category = getattr(field, 'category', None)
            if category not in grouped_data:
                grouped_data[category] = []
            remarks_field = f"{field.name}_remarks"
            grouped_data[category].append((
                field.verbose_name,
                getattr(report, field.name),
                getattr(report, remarks_field, "")
            ))

    for category_code, entries in grouped_data.items():
        label = CATEGORY_LABELS.get(category_code, category_code)
        ws.append([label])
        ws.append(['Question', 'Answer', 'Remarks'])
        for q, a, r in entries:
            ws.append([q, a, r])
        ws.append([])

    wb.save(response)
    return response




def export_csv(request, report_id):
    report = WalkthroughReport.objects.get(pk=report_id)
    data = get_verbose_data(report)

    response = HttpResponse(content_type='text/csv')
    filename = f"walkthrough_report_{report_id}.csv"
    response['Content-Disposition'] = f'attachment; filename={filename}'

    writer = csv.writer(response)
    
    # Adding a title row
    writer.writerow(["🏠 Walkthrough Report"])
    writer.writerow([])  # Blank row for spacing
    
    # Add headers (emphasizing structure)
    writer.writerow(['Category', 'Question', 'Answer', 'Remarks'])

    # Group data by category and write to the CSV
    grouped = {}
    for question, answer, remark, category in data:
        if category not in grouped:
            grouped[category] = []
        grouped[category].append((question, answer, remark))

    # Add each category and its rows without unwanted emoji or label
    for category, rows in grouped.items():
        # Get category label without any unwanted prefix (emoji or special chars)
        label = CATEGORY_LABELS.get(category, category).replace("📌", "").strip()  # Remove unwanted parts

        writer.writerow([label])  # Only the clean category name
        for question, answer, remark in rows:
            writer.writerow([category, question, answer, remark or "-"])
        writer.writerow([])  # Blank row to separate categories

    return response
# Creating Reports 
from django.shortcuts import render, get_object_or_404
from django.db.models.functions import TruncMonth
from django.db.models import DateTimeField
from django.db.models import F

def all_reports_view(request):
    reports = WalkthroughReport.objects.select_related("property").order_by("-datetime")

    # PROPERTY FILTER
    property_id = request.GET.get("property")
    if property_id:
        reports = reports.filter(property_id=property_id)

    # MONTH FILTER (YYYY-MM)
    month = request.GET.get("month")
    if month:
        year, month_num = month.split("-")
        reports = reports.filter(
            datetime__year=year,
            datetime__month=month_num
        )

    # ALL USER PROPERTIES (FOR DROPDOWN)
    properties = PropertyManagement.objects.all()

    # AVAILABLE MONTHS (ONLY MONTHS THAT EXIST IN REPORTS)
    months = (
        WalkthroughReport.objects
        .annotate(month=TruncMonth("datetime"))
        .values_list("month", flat=True)
        .distinct()
        .order_by("-month")
    )

    return render(
        request,
        "mainapp/walktrug/all_reports.html",
        {
            "reports": reports,
            "properties": properties,
            "months": months,
        }
    )

from walkthroughreport.models import GeneralItemsExterior
from django.shortcuts import get_object_or_404, render
def report_detail_view(request, pk):
    report = get_object_or_404(WalkthroughReport, pk=pk)
    
    # Define all related model mappings
    related_models = {
        'general_items_exterior': {
            'prefix': 'gie',
            'count': 15
        },
        'general_items_interior': {
            'prefix': 'gii',
            'count': 10
        },
        'garage': {
            'prefix': 'garage',
            'count': 9
        },
        'laundry': {
            'prefix': 'laundry',
            'count': 6
        },
        'kitchen': {
            'prefix': 'kitchen',
            'count': 14
        },
        'butlers': {
            'prefix': 'butlers',
            'count': 12
        },
        'breakfast_area': {
            'prefix': 'breakfast',
            'count': 7
        },
        'entry_foyer': {
            'prefix': 'entry',
            'count': 6
        },
        'great_room': {
            'prefix': 'greatroom',
            'count': 7
        },
        'dining_room': {
            'prefix': 'dining',
            'count': 7
        },
        'closets_main_level': {
            'prefix': 'closets',
            'count': 5
        },
        'closets_upper_level': {
            'prefix': 'closets_upper',
            'count': 5
        },
        'hallways_main_level': {
            'prefix': 'hallways_main',
            'count': 5
        },
        'hallways_upper_level': {
            'prefix': 'hallways_upper',
            'count': 5
        },
        'bedroom1': {
            'prefix': 'bedroom1_',
            'count': 4
        },
        'bedroom2': {
            'prefix': 'bedroom2_',
            'count': 4
        },
        'bedroom3': {
            'prefix': 'bedroom3_',
            'count': 4
        },
        'bedroom4': {
            'prefix': 'bedroom4_',
            'count': 4
        },
        'bedroom5': {
            'prefix': 'bedroom5_',
            'count': 6
        },
        'bedroom6': {
            'prefix': 'bedroom6_',
            'count': 6
        },
        'bedroom7': {
            'prefix': 'bedroom7_',
            'count': 6
        },
        'bedroom8': {
            'prefix': 'bedroom8_',
            'count': 6
        },
        'bedroom9': {
            'prefix': 'bedroom9_',
            'count': 6
        },
        'bedroom10': {
            'prefix': 'bedroom10_',
            'count': 6
        },
        'bathroom1': {
            'prefix': 'bathroom1_',
            'count': 8
        },
        'bathroom2': {
            'prefix': 'bathroom2_',
            'count': 8
        },
        'bathroom3': {
            'prefix': 'bathroom3_',
            'count': 8
        },
        'bathroom4': {
            'prefix': 'bathroom4_',
            'count': 8
        },
        'bathroom5': {
            'prefix': 'bathroom5_',
            'count': 8
        },
        'bathroom6': {
            'prefix': 'bathroom6_',
            'count': 10
        },
        'bathroom7': {
            'prefix': 'bathroom7_',
            'count': 10
        },
        'bathroom8': {
            'prefix': 'bathroom8_',
            'count': 10
        },
        'bathroom9': {
            'prefix': 'bathroom9_',
            'count': 10
        },
        'bathroom10': {
            'prefix': 'bathroom10_',
            'count': 10
        },
        'bathroom11': {
            'prefix': 'bathroom11_',
            'count': 10
        },
        'bathroom12': {
            'prefix': 'bathroom12_',
            'count': 10
        },
        'gym': {
            'prefix': 'gym_',
            'count': 9  # Changed from 7 to 9
        },
        'theatre_music_room': {  # Changed from 'theatre' to 'theatre_music_room'
            'prefix': 'theatre_',
            'count': 7
        },
        'guest_house_sleeping_living': {  # Changed from 'guest_house' to 'guest_house_sleeping_living'
            'prefix': 'guest_house_',
            'count': 7  # Changed from 5 to 7
        },
        'guest_house_bathroom': {  # Changed from 'guest_house_bath' to 'guest_house_bathroom'
            'prefix': 'guest_house_bath_',
            'count': 10  # Changed from 8 to 10
        }
    }
    
    # Flatten all fields from related models
    for related_name, config in related_models.items():
        if hasattr(report, related_name):
            related_obj = getattr(report, related_name)
            prefix = config['prefix']
            count = config['count']
            
            for i in range(1, count + 1):
                field_name = f'{prefix}{i}'
                setattr(report, field_name, getattr(related_obj, field_name, None))
                setattr(report, f'{field_name}_remarks', getattr(related_obj, f'{field_name}_remarks', None))
    
    context = {
        'report': report,
        'client_first_name': report.user.first_name if report.user else '',
        'client_last_name': report.user.last_name if report.user else '',
        'report_datetime': report.datetime.strftime('%Y-%m-%d') if report.datetime else 'No Datetime Available',
        'report_description': report.description if report.description else 'Walkthrough Report',
        'report_property': str(report.property) if report.property else 'Walkthrough Report',
    }
    
    return render(request, 'mainapp/walktrug/report_detail.html', context)


def open_reports_view(request):
    reports = WalkthroughReport.objects.filter(status='Open').select_related("property").order_by("-datetime")

    # PROPERTY FILTER
    property_id = request.GET.get("property")
    if property_id:
        reports = reports.filter(property_id=property_id)

    # MONTH FILTER
    month = request.GET.get("month")
    if month:
        year, month_num = month.split("-")
        reports = reports.filter(datetime__year=year, datetime__month=month_num)

    # ALL PROPERTIES
    properties = PropertyManagement.objects.all()

    # AVAILABLE MONTHS
    months = (
        WalkthroughReport.objects.filter(status='Open')
        .annotate(month=TruncMonth("datetime"))
        .values_list("month", flat=True)
        .distinct()
        .order_by("-month")
    )

    return render(request, 'mainapp/walktrug/open_reports.html', {
        'reports': reports,
        'properties': properties,
        'months': months,
    })


def completed_reports_view(request):
    reports = WalkthroughReport.objects.filter(status='Completed').select_related("property").order_by("-datetime")

    # PROPERTY FILTER
    property_id = request.GET.get("property")
    if property_id:
        reports = reports.filter(property_id=property_id)

    # MONTH FILTER
    month = request.GET.get("month")
    if month:
        year, month_num = month.split("-")
        reports = reports.filter(datetime__year=year, datetime__month=month_num)

    # ALL PROPERTIES
    properties = PropertyManagement.objects.all()

    # AVAILABLE MONTHS
    months = (
        WalkthroughReport.objects.filter(status='Completed')
        .annotate(month=TruncMonth("datetime"))
        .values_list("month", flat=True)
        .distinct()
        .order_by("-month")
    )

    return render(request, 'mainapp/walktrug/completed_reports.html', {
        'reports': reports,
        'properties': properties,
        'months': months,
    })


def denied_reports_view(request):
    reports = WalkthroughReport.objects.filter(status='Denied').select_related("property").order_by("-datetime")

    # PROPERTY FILTER
    property_id = request.GET.get("property")
    if property_id:
        reports = reports.filter(property_id=property_id)

    # MONTH FILTER
    month = request.GET.get("month")
    if month:
        year, month_num = month.split("-")
        reports = reports.filter(datetime__year=year, datetime__month=month_num)

    # ALL PROPERTIES
    properties = PropertyManagement.objects.all()

    # AVAILABLE MONTHS
    months = (
        WalkthroughReport.objects.filter(status='Denied')
        .annotate(month=TruncMonth("datetime"))
        .values_list("month", flat=True)
        .distinct()
        .order_by("-month")
    )

    return render(request, 'mainapp/walktrug/denied_reports.html', {
        'reports': reports,
        'properties': properties,
        'months': months,
    })
# Sending emails 
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def update_report_status(request, report_id, status):
    """
    Update the status of a WalkthroughReport to either 'Completed' or 'Denied'
    """
    # Get the report object or return 404
    report = get_object_or_404(WalkthroughReport, pk=report_id)
    
    # Validate the status
    if status in ['Pending', 'Denied']:
        report.status = status
        report.save()
        messages.success(request, f"Report status updated to {status}")
    else:
        messages.error(request, "Invalid status option")
    
    # Redirect back to the previous page
    return redirect(request.META.get('HTTP_REFERER', 'mainapp:report_list'))

def privacy_view(request):
    return render(request, 'privacy.html')




# Walkthrough-Report SETUP ----------------------------------------------------------------------------------- CLIENT SIDE START --


CATEGORY_MAP = {
    'gie': "General Items - Exterior",
    'gii': "General Items - Interior", 
    'garage': "Garage",
    'laundry': "Laundry / Mudroom",
    'kitchen': "Kitchen",
    'butlers': "Butlers",
    'breakfast': "Breakfast Area",
    'entry': "Entry / Foyer",
    'great': "Great Room / Family Room",
    'dining': "Dining Room / Area",
    'closets_main': "Closets - Main Level",
    'closets_upper': "Closets - Upper Level",
    'hallways_main': "Hallways - Main Level",
    'hallways_upper': "Hallways - Upper Level",
    'bedroom1': "Bedroom 1 (Master Bedroom)",
    'bedroom2': "Bedroom 2",
    'bedroom3': "Bedroom 3",
    'bedroom4': "Bedroom 4",
    'bedroom5': "Bedroom 5",
    'bedroom6': "Bedroom 6",
    'bedroom7': "Bedroom 7",
    'bedroom8': "Bedroom 8",
    'bedroom9': "Bedroom 9",
    'bedroom10': "Bedroom 10",
    'bathroom1': "Bathroom 1 (Master Bath)",
    'bathroom2': "Bathroom 2",
    'bathroom3': "Bathroom 3",
    'bathroom4': "Bathroom 4",
    'bathroom5': "Bathroom 5",
    'bathroom6': "Bathroom 6",
    'bathroom7': "Bathroom 7",
    'bathroom8': "Bathroom 8",
    'bathroom9': "Bathroom 9",
    'bathroom10': "Bathroom 10",
    'bathroom11': "Bathroom 11",
    'bathroom12': "Bathroom 12",
    'gym': "Gym",
    'theatre': "Theatre / Music Room",
    'music': "Theatre / Music Room",
    'guest_house_sleeping': "Guest House - Sleeping / Living",
    'guest_house_living': "Guest House - Sleeping / Living",
    'guest_house_bathroom': "Guest House - Bathroom",
}

from django.db.models import Q
from walkthroughreport.models import (
    WalkthroughReport, GeneralItemsExterior, GeneralItemsInterior,
    Garage, Laundry, Kitchen, Butlers, BreakfastArea, EntryFoyer,
    GreatRoom, DiningRoom, ClosetsMainLevel, ClosetsUpperLevel,
    HallwaysMainLevel, HallwaysUpperLevel, Bedroom1, Bedroom2, Bedroom3,
    Bedroom4, Bedroom5, Bedroom6, Bedroom7, Bedroom8, Bedroom9, Bedroom10,
    Bathroom1, Bathroom2, Bathroom3, Bathroom4, Bathroom5, Bathroom6,
    Bathroom7, Bathroom8, Bathroom9, Bathroom10, Bathroom11, Bathroom12,
    Gym, TheatreMusicRoom, GuestHouseSleepingLiving, GuestHouseBathroom
)

def get_category_from_model_name(model_name):
    """Get category name from model name"""
    model_to_category = {
        'GeneralItemsExterior': 'gie',
        'GeneralItemsInterior': 'gii',
        'Garage': 'garage',
        'Laundry': 'laundry',
        'Kitchen': 'kitchen',
        'Butlers': 'butlers',
        'BreakfastArea': 'breakfast',
        'EntryFoyer': 'entry',
        'GreatRoom': 'great',
        'DiningRoom': 'dining',
        'ClosetsMainLevel': 'closets_main',
        'ClosetsUpperLevel': 'closets_upper',
        'HallwaysMainLevel': 'hallways_main',
        'HallwaysUpperLevel': 'hallways_upper',
        'Bedroom1': 'bedroom1',
        'Bedroom2': 'bedroom2',
        'Bedroom3': 'bedroom3',
        'Bedroom4': 'bedroom4',
        'Bedroom5': 'bedroom5',
        'Bedroom6': 'bedroom6',  
        'Bedroom7': 'bedroom7',
        'Bedroom8': 'bedroom8',
        'Bedroom9': 'bedroom9',
        'Bedroom10': 'bedroom10',
        'Bathroom1': 'bathroom1',
        'Bathroom2': 'bathroom2',
        'Bathroom3': 'bathroom3',
        'Bathroom4': 'bathroom4',
        'Bathroom5': 'bathroom5',
        'Bathroom6': 'bathroom6',
        'Bathroom7': 'bathroom7',
        'Bathroom8': 'bathroom8',
        'Bathroom9': 'bathroom9',
        'Bathroom10': 'bathroom10',
        'Bathroom11': 'bathroom11',
        'Bathroom12': 'bathroom12',
        'Gym': 'gym',
        'TheatreMusicRoom': 'theatre',
        'GuestHouseSleepingLiving': 'guest_house_sleeping',
        'GuestHouseBathroom': 'guest_house_bathroom',
    }
    return model_to_category.get(model_name, model_name.lower())

def process_model_fields(model_instance, report, model_name):
    """Process fields from a specific model and return inspection items"""
    inspection_items = []
    category_key = get_category_from_model_name(model_name)
    category = CATEGORY_MAP.get(category_key, model_name)
    
    for field in model_instance._meta.get_fields():
        field_name = field.name
        
        # Skip non-relevant fields
        if (
            field_name in ['id', 'walkthrough_report'] or
            field_name.endswith('_remarks') or
            field_name.endswith('_amount') or
            field_name.endswith('_calculation_note') or
            field_name.endswith('_client_approval') or
            field_name.endswith('_udpate_status') or
            field_name.endswith('_update_date') or
            field_name.endswith('_update_remarks')
        ):
            continue
        
        field_value = getattr(model_instance, field_name, None)
        if field_value != "Non-Compliant":
            continue
        
        # Get related fields
        base = field_name
        remarks = getattr(model_instance, f"{base}_remarks", '')
        amount = getattr(model_instance, f"{base}_amount", None)
        calculation_note = getattr(model_instance, f"{base}_calculation_note", '')
        client_approval = getattr(model_instance, f"{base}_client_approval", '')
        update_status = getattr(model_instance, f"{base}_udpate_status", '')
        update_date = getattr(model_instance, f"{base}_update_date", None)
        update_remarks = getattr(model_instance, f"{base}_update_remarks", '')
        
        # Human-readable question
        verbose_name = field.verbose_name if hasattr(field, 'verbose_name') else base.replace('_', ' ').title()
        
        inspection_items.append({
            'category': category,
            'question': verbose_name,
            'remarks': remarks,
            'amount': amount,
            'calculation_note': calculation_note,
            'client_approval': client_approval,
            'update_status': update_status,
            'update_date': update_date,
            'update_remarks': update_remarks,
            'value': field_value,
            'field_name': base,
            'model_name': model_name,
            'model_id': model_instance.id,
            'completion_date': update_date,  # Add this
        })
    
    return inspection_items

def walktrug_open_reports_view(request):
    reports = WalkthroughReport.objects.filter(user_id=request.session.get('client_id')).filter(
        Q(status__in=['Open', 'Completed']) | 
        Q(item_status_check=False)
    ).select_related('user', 'property')
    
    processed_reports = []
    
    # All related models to check
    related_models = [
        (GeneralItemsExterior, 'general_items_exterior'),
        (GeneralItemsInterior, 'general_items_interior'),
        (Garage, 'garage'),
        (Laundry, 'laundry'),
        (Kitchen, 'kitchen'),
        (Butlers, 'butlers'),
        (BreakfastArea, 'breakfast_area'),
        (EntryFoyer, 'entry_foyer'),
        (GreatRoom, 'great_room'),
        (DiningRoom, 'dining_room'),
        (ClosetsMainLevel, 'closets_main_level'),
        (ClosetsUpperLevel, 'closets_upper_level'),
        (HallwaysMainLevel, 'hallways_main_level'),
        (HallwaysUpperLevel, 'hallways_upper_level'),
        (Bedroom1, 'bedroom1'),
        (Bedroom2, 'bedroom2'),
        (Bedroom3, 'bedroom3'),
        (Bedroom4, 'bedroom4'),
        (Bedroom5, 'bedroom5'),
        (Bedroom6, 'bedroom6'),
        (Bedroom7, 'bedroom7'),
        (Bedroom8, 'bedroom8'),
        (Bedroom9, 'bedroom9'),
        (Bedroom10, 'bedroom10'),
        (Bathroom1, 'bathroom1'),
        (Bathroom2, 'bathroom2'),
        (Bathroom3, 'bathroom3'),
        (Bathroom4, 'bathroom4'),
        (Bathroom5, 'bathroom5'),
        (Bathroom6, 'bathroom6'),
        (Bathroom7, 'bathroom7'),
        (Bathroom8, 'bathroom8'),
        (Bathroom9, 'bathroom9'),
        (Bathroom10, 'bathroom10'),
        (Bathroom11, 'bathroom11'),
        (Bathroom12, 'bathroom12'),
        (Gym, 'gym'),
        (TheatreMusicRoom, 'theatre_music_room'),
        (GuestHouseSleepingLiving, 'guest_house_sleeping_living'),
        (GuestHouseBathroom, 'guest_house_bathroom'),
    ]
    
    for report in reports:
        all_inspection_items = []
        
        # Process each related model
        for model_class, relation_name in related_models:
            try:
                # Get the related model instance
                model_instance = getattr(report, relation_name, None)
                if model_instance:
                    items = process_model_fields(model_instance, report, model_class.__name__)
                    all_inspection_items.extend(items)
            except Exception as e:
                # Handle cases where relation doesn't exist
                continue
        
        # Only add reports that have inspection items
        if all_inspection_items:
            report.inspection_items = all_inspection_items
            processed_reports.append(report)
    
    return render(request, 'mainapp/walktrug/open_items.html', {'reports': processed_reports})

def walktrug_completed_reports_view(request):
    reports = WalkthroughReport.objects.filter(user_id=request.session.get('client_id')).filter(
        Q(status__in=['Open', 'Completed']) | 
        Q(item_status_check=False)
    ).select_related('user', 'property')
    
    processed_reports = []
    
    # All related models to check
    related_models = [
        (GeneralItemsExterior, 'general_items_exterior'),
        (GeneralItemsInterior, 'general_items_interior'),
        (Garage, 'garage'),
        (Laundry, 'laundry'),
        (Kitchen, 'kitchen'),
        (Butlers, 'butlers'),
        (BreakfastArea, 'breakfast_area'),
        (EntryFoyer, 'entry_foyer'),
        (GreatRoom, 'great_room'),
        (DiningRoom, 'dining_room'),
        (ClosetsMainLevel, 'closets_main_level'),
        (ClosetsUpperLevel, 'closets_upper_level'),
        (HallwaysMainLevel, 'hallways_main_level'),
        (HallwaysUpperLevel, 'hallways_upper_level'),
        (Bedroom1, 'bedroom1'),
        (Bedroom2, 'bedroom2'),
        (Bedroom3, 'bedroom3'),
        (Bedroom4, 'bedroom4'),
        (Bedroom5, 'bedroom5'),
        (Bedroom6, 'bedroom6'),
        (Bedroom7, 'bedroom7'),
        (Bedroom8, 'bedroom8'),
        (Bedroom9, 'bedroom9'),
        (Bedroom10, 'bedroom10'),
        (Bathroom1, 'bathroom1'),
        (Bathroom2, 'bathroom2'),
        (Bathroom3, 'bathroom3'),
        (Bathroom4, 'bathroom4'),
        (Bathroom5, 'bathroom5'),
        (Bathroom6, 'bathroom6'),
        (Bathroom7, 'bathroom7'),
        (Bathroom8, 'bathroom8'),
        (Bathroom9, 'bathroom9'),
        (Bathroom10, 'bathroom10'),
        (Bathroom11, 'bathroom11'),
        (Bathroom12, 'bathroom12'),
        (Gym, 'gym'),
        (TheatreMusicRoom, 'theatre_music_room'),
        (GuestHouseSleepingLiving, 'guest_house_sleeping_living'),
        (GuestHouseBathroom, 'guest_house_bathroom'),
    ]
    
    for report in reports:
        all_inspection_items = []
        
        # Process each related model
        for model_class, relation_name in related_models:
            try:
                # Get the related model instance
                model_instance = getattr(report, relation_name, None)
                if model_instance:
                    items = process_model_fields(model_instance, report, model_class.__name__)
                    all_inspection_items.extend(items)
            except Exception as e:
                # Handle cases where relation doesn't exist
                continue
        
        # Only add reports that have inspection items
        if all_inspection_items:
            report.inspection_items = all_inspection_items
            processed_reports.append(report)
    
    return render(request, 'mainapp/walktrug/completed_items.html', {'reports': processed_reports})

def walktrug_denied_reports_view(request):
    reports = WalkthroughReport.objects.filter(user_id=request.session.get('client_id')).filter(
        Q(status__in=['Open', 'Completed']) | 
        Q(item_status_check=False)
    ).select_related('user', 'property')
    
    processed_reports = []
    
    # All related models to check
    related_models = [
        (GeneralItemsExterior, 'general_items_exterior'),
        (GeneralItemsInterior, 'general_items_interior'),
        (Garage, 'garage'),
        (Laundry, 'laundry'),
        (Kitchen, 'kitchen'),
        (Butlers, 'butlers'),
        (BreakfastArea, 'breakfast_area'),
        (EntryFoyer, 'entry_foyer'),
        (GreatRoom, 'great_room'),
        (DiningRoom, 'dining_room'),
        (ClosetsMainLevel, 'closets_main_level'),
        (ClosetsUpperLevel, 'closets_upper_level'),
        (HallwaysMainLevel, 'hallways_main_level'),
        (HallwaysUpperLevel, 'hallways_upper_level'),
        (Bedroom1, 'bedroom1'),
        (Bedroom2, 'bedroom2'),
        (Bedroom3, 'bedroom3'),
        (Bedroom4, 'bedroom4'),
        (Bedroom5, 'bedroom5'),
        (Bedroom6, 'bedroom6'),
        (Bedroom7, 'bedroom7'),
        (Bedroom8, 'bedroom8'),
        (Bedroom9, 'bedroom9'),
        (Bedroom10, 'bedroom10'),
        (Bathroom1, 'bathroom1'),
        (Bathroom2, 'bathroom2'),
        (Bathroom3, 'bathroom3'),
        (Bathroom4, 'bathroom4'),
        (Bathroom5, 'bathroom5'),
        (Bathroom6, 'bathroom6'),
        (Bathroom7, 'bathroom7'),
        (Bathroom8, 'bathroom8'),
        (Bathroom9, 'bathroom9'),
        (Bathroom10, 'bathroom10'),
        (Bathroom11, 'bathroom11'),
        (Bathroom12, 'bathroom12'),
        (Gym, 'gym'),
        (TheatreMusicRoom, 'theatre_music_room'),
        (GuestHouseSleepingLiving, 'guest_house_sleeping_living'),
        (GuestHouseBathroom, 'guest_house_bathroom'),
    ]
    
    for report in reports:
        all_inspection_items = []
        
        # Process each related model
        for model_class, relation_name in related_models:
            try:
                # Get the related model instance
                model_instance = getattr(report, relation_name, None)
                if model_instance:
                    items = process_model_fields(model_instance, report, model_class.__name__)
                    all_inspection_items.extend(items)
            except Exception as e:
                # Handle cases where relation doesn't exist
                continue
        
        # Only add reports that have inspection items
        if all_inspection_items:
            report.inspection_items = all_inspection_items
            processed_reports.append(report)
    
    return render(request, 'mainapp/walktrug/denied_items.html', {'reports': processed_reports})



from django.http import JsonResponse
import json


@csrf_exempt
def update_client_approval(request, report_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    try:
        data = json.loads(request.body)
        field_name = data.get('field_name')
        client_approval = data.get('client_approval')
        category = data.get('category')

        if client_approval not in ['Approved', 'Denied', 'Cost']:
            return JsonResponse({'status': 'error', 'message': 'Invalid approval'}, status=400)

        report = WalkthroughReport.objects.get(id=report_id)

        def normalize_category(cat):
            if 'Voyer' in cat:
                cat = cat.replace('Voyer', 'Foyer')
            return cat

        category = normalize_category(category)

        model_mapping = {
            'General Items - Exterior': GeneralItemsExterior,
            'General Items - Interior': GeneralItemsInterior,
            'Garage': Garage,
            'Laundry / Mudroom': Laundry,
            'Kitchen': Kitchen,
            'Butlers': Butlers,
            'Breakfast Area': BreakfastArea,
            'Entry / Foyer': EntryFoyer,
            'Great Room / Family Room': GreatRoom,
            'Dining Room / Area': DiningRoom,
            'Closets - Main Level': ClosetsMainLevel,
            'Closets - Upper Level': ClosetsUpperLevel,
            'Hallways - Main Level': HallwaysMainLevel,
            'Hallways - Upper Level': HallwaysUpperLevel,
            'Bedroom 1 (Master Bedroom)': Bedroom1,
            'Bedroom 2': Bedroom2,
            'Bedroom 3': Bedroom3,
            'Bedroom 4': Bedroom4,
            'Bedroom 5': Bedroom5,
            'Bedroom 6': Bedroom6,
            'Bedroom 7': Bedroom7,
            'Bedroom 8': Bedroom8,
            'Bedroom 9': Bedroom9,
            'Bedroom 10': Bedroom10,
            'Bathroom 1 (Master Bath)': Bathroom1,
            'Bathroom 2': Bathroom2,
            'Bathroom 3': Bathroom3,
            'Bathroom 4': Bathroom4,
            'Bathroom 5': Bathroom5,
            'Bathroom 6': Bathroom6,
            'Bathroom 7': Bathroom7,
            'Bathroom 8': Bathroom8,
            'Bathroom 9': Bathroom9,
            'Bathroom 10': Bathroom10,
            'Bathroom 11': Bathroom11,
            'Bathroom 12': Bathroom12,
            'Gym': Gym,
            'Theatre / Music Room': TheatreMusicRoom,
            'Guest House - Sleeping / Living': GuestHouseSleepingLiving,
            'Guest House - Bathroom': GuestHouseBathroom,
        }

        if category not in model_mapping:
            return JsonResponse({'status': 'error', 'message': 'Invalid category'}, status=400)

        model_class = model_mapping[category]
        instance, _ = model_class.objects.get_or_create(walkthrough_report=report)

        approval_field = f"{field_name}_client_approval"
        if not hasattr(instance, approval_field):
            return JsonResponse({'status': 'error', 'message': 'Invalid field'}, status=400)

        setattr(instance, approval_field, client_approval)
        instance.save()

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
# Walkthrough-Report SETUP ----------------------------------------------------------------------------------- CLIENT SIDE END --
