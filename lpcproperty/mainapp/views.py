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

from django.contrib.auth.hashers import check_password

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
                "noreply@yourdomain.com",
                [email],
            )
            messages.success(request, "OTP sent to your email.")
            return redirect("client_password_verify")
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
            return redirect("login")  # update with your login view name
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

def client_properties(request):
    client_id = request.session['client_id']
    client = Client.objects.get(id=client_id)

    properties = PropertyManagement.objects.filter(client=client).prefetch_related('floors__rooms', 'client_manager')

    contacts = [
        {"name": client.contact1_name, "email": client.contact1_email, "phone": client.contact1_phone, "preferred": client.contact1_preferred},
        {"name": client.contact2_name, "email": client.contact2_email, "phone": client.contact2_phone, "preferred": client.contact2_preferred},
        {"name": client.contact3_name, "email": client.contact3_email, "phone": client.contact3_phone, "preferred": client.contact3_preferred},
    ]
    contacts = [c for c in contacts if c["name"]]

    # Get manager from the first property (if exists)
    client_manager = properties[0].client_manager if properties else None

    return render(request, 'property/properties.html', {
        'properties': properties,
        'contacts': contacts,
        'client_manager': client_manager,
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

def all_reports_view(request):
    reports = WalkthroughReport.objects.all()
    return render(request, 'mainapp/walktrug/all_reports.html', {'reports': reports})

# def report_detail_view(request, pk):
#     report = get_object_or_404(WalkthroughReport, pk=pk)
#     return render(request, 'mainapp/walktrug/report_detail.html', {'report': report})
import copy
def report_detail_view(request, pk):
    report = get_object_or_404(WalkthroughReport, pk=pk)
    
    # Create a modified version for the template
    filtered_report = copy.deepcopy(report)
    
    # Loop through all fields in the model
    for field_name in dir(filtered_report):
        # Skip private/internal attributes and remarks fields
        if field_name.startswith('_') or field_name.endswith('_remarks'):
            continue
        
        field_value = getattr(filtered_report, field_name, None)
        # Set to None if not "Non-Compliant"
        if field_value is not None and field_value != "Non-Compliant":
            setattr(filtered_report, field_name, None)
    
    # Ensure the report object still has a valid pk (ID) for URL generation
    if not filtered_report.pk:
        filtered_report.pk = report.pk
     # Access the user's first and last name via the foreign key
    client_first_name = report.user.first_name if report.user else ''
    client_last_name = report.user.last_name if report.user else ''
    report_description = report.description if report.description else 'Walkthrough Report'
    report_property = report.property if report.property else 'Walkthrough Report'

    # Access the datetime field
   # Modify the datetime format to show only the date (Year-Month-Day)
    report_datetime = report.datetime.strftime('%Y-%m-%d') if report.datetime else 'No Datetime Available'

    return render(request, 'mainapp/walktrug/report_detail.html', {'report': filtered_report,'client_first_name': client_first_name,
        'client_last_name': client_last_name,'report_datetime': report_datetime,'report_description':report_description,'report_property':report_property}) 


def completed_reports_view(request):
    reports = WalkthroughReport.objects.filter(status='Completed')
    return render(request, 'mainapp/walktrug/completed_reports.html', {'reports': reports})

def denied_reports_view(request):
    reports = WalkthroughReport.objects.filter(status='Denied')
    return render(request, 'mainapp/walktrug/denied_reports.html', {'reports': reports})

def open_reports_view(request):
    reports = WalkthroughReport.objects.filter(status='Open')
    return render(request, 'mainapp/walktrug/open_reports.html', {'reports': reports})


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