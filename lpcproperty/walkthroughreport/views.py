from django.shortcuts import render

# Create your views here.
# views.py

from django.shortcuts import render
from .models import WalkthroughReport
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from django.shortcuts import render
from django.http import HttpResponse
from .models import WalkthroughReport
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
from .models import WalkthroughReport

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
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from django.http import HttpResponse

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

def get_verbose_data_from_models(report):
    """
    Extract data from all related models and format it for PDF generation
    """
    data = []
    
    # All related models mapping
    related_models = [
        (GeneralItemsExterior, 'general_items_exterior', 'General Items - Exterior'),
        (GeneralItemsInterior, 'general_items_interior', 'General Items - Interior'),
        (Garage, 'garage', 'Garage'),
        (Laundry, 'laundry', 'Laundry / Mudroom'),
        (Kitchen, 'kitchen', 'Kitchen'),
        (Butlers, 'butlers', 'Butlers'),
        (BreakfastArea, 'breakfast_area', 'Breakfast Area'),
        (EntryFoyer, 'entry_foyer', 'Entry / Foyer'),
        (GreatRoom, 'great_room', 'Great Room / Family Room'),
        (DiningRoom, 'dining_room', 'Dining Room / Area'),
        (ClosetsMainLevel, 'closets_main_level', 'Closets - Main Level'),
        (ClosetsUpperLevel, 'closets_upper_level', 'Closets - Upper Level'),
        (HallwaysMainLevel, 'hallways_main_level', 'Hallways - Main Level'),
        (HallwaysUpperLevel, 'hallways_upper_level', 'Hallways - Upper Level'),
        (Bedroom1, 'bedroom1', 'Bedroom 1 (Master Bedroom)'),
        (Bedroom2, 'bedroom2', 'Bedroom 2'),
        (Bedroom3, 'bedroom3', 'Bedroom 3'),
        (Bedroom4, 'bedroom4', 'Bedroom 4'),
        (Bedroom5, 'bedroom5', 'Bedroom 5'),
        (Bedroom6, 'bedroom6', 'Bedroom 6'),
        (Bedroom7, 'bedroom7', 'Bedroom 7'),
        (Bedroom8, 'bedroom8', 'Bedroom 8'),
        (Bedroom9, 'bedroom9', 'Bedroom 9'),
        (Bedroom10, 'bedroom10', 'Bedroom 10'),
        (Bathroom1, 'bathroom1', 'Bathroom 1 (Master Bath)'),
        (Bathroom2, 'bathroom2', 'Bathroom 2'),
        (Bathroom3, 'bathroom3', 'Bathroom 3'),
        (Bathroom4, 'bathroom4', 'Bathroom 4'),
        (Bathroom5, 'bathroom5', 'Bathroom 5'),
        (Bathroom6, 'bathroom6', 'Bathroom 6'),
        (Bathroom7, 'bathroom7', 'Bathroom 7'),
        (Bathroom8, 'bathroom8', 'Bathroom 8'),
        (Bathroom9, 'bathroom9', 'Bathroom 9'),
        (Bathroom10, 'bathroom10', 'Bathroom 10'),
        (Bathroom11, 'bathroom11', 'Bathroom 11'),
        (Bathroom12, 'bathroom12', 'Bathroom 12'),
        (Gym, 'gym', 'Gym'),
        (TheatreMusicRoom, 'theatre_music_room', 'Theatre / Music Room'),
        (GuestHouseSleepingLiving, 'guest_house_sleeping_living', 'Guest House - Sleeping / Living'),
        (GuestHouseBathroom, 'guest_house_bathroom', 'Guest House - Bathroom'),
    ]
    
    for model_class, relation_name, display_name in related_models:
        try:
            model_instance = getattr(report, relation_name, None)
            
            if model_instance:
                for field in model_instance._meta.fields:
                    name = field.name
                    if name[-1:].isdigit() and not name.endswith('_remarks'):
                        answer = getattr(model_instance, name)
                        remark = getattr(model_instance, f"{name}_remarks", '')

                        if answer:
                            verbose = field.verbose_name or name.replace('_', ' ').capitalize()
                            data.append((verbose, answer, remark, display_name))
                    
        except Exception as e:
            continue
    
    return data


def export_pdf(request, report_id):
    import re
    
    report = WalkthroughReport.objects.get(pk=report_id)
    
    # Get all data from multiple models instead of single model
    data = get_verbose_data_from_models(report)
    
    # Get client name details
    client_first_name = report.user.first_name if report.user else ''
    client_last_name = report.user.last_name if report.user else ''
    client_name = f"{client_first_name} {client_last_name}".strip() or "N/A"
    
    # Format report date
    report_date = report.datetime.strftime('%Y-%m-%d') if report.datetime else 'N/A'
    
    # Get property information if available
    property_info = report.property.name if hasattr(report.property, 'name') else getattr(report.property, 'address', 'N/A')
    if callable(property_info):
        property_info = property_info()
    
    # Get report description (inspection note)
    inspection_note = getattr(report, 'description', '')

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

    # Styles for different elements
    styles.add(ParagraphStyle(
        name='GreenTitle',
        fontSize=16,
        leading=18,
        textColor=colors.HexColor("#2e7d32"),
        fontName="Helvetica-Bold",
        alignment=1,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontSize=12,
        leading=15,
        spaceAfter=10,
        textColor=colors.HexColor("#003366"),
        fontName="Helvetica-Bold",
        borderPadding=(0, 0, 0, 4),
        borderWidth=0,
        borderColor=colors.HexColor("#003366"),
        borderRadius=None
    ))
    
    styles.add(ParagraphStyle(
        name='ReportInfo',
        fontSize=10,
        leading=12,
        spaceAfter=2,
        fontName="Helvetica",
    ))

    wrap_style = ParagraphStyle(
        name='wrapped',
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        wordWrap='CJK',
    )

    # Main heading with property name
    elements.append(Paragraph(f"🏠 {property_info}", styles['GreenTitle']))

    # Underline
    elements.append(Table([[""]], colWidths=[6.3 * inch], style=[
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor("#2e7d32"))],
    ))
    elements.append(Spacer(1, 12))
    
    # Report details section
    elements.append(Paragraph("Report Details:", styles['SectionTitle']))
    elements.append(Paragraph(f"<b>Client:</b> {client_name}", styles['ReportInfo']))
    elements.append(Paragraph(f"<b>Date:</b> {report_date}", styles['ReportInfo']))
    elements.append(Paragraph(f"<b>Inspection Note:</b> {inspection_note}", styles['ReportInfo']))
    
    elements.append(Spacer(1, 20))
    
    # Report contents title
    elements.append(Paragraph("Report Contents", styles['SectionTitle']))
    elements.append(Spacer(1, 10))

    # Grouping data by exact category name while preserving order
    grouped = {}
    category_order = []
    
    for question, answer, remark, category in data:
        if category not in grouped:
            grouped[category] = []
            category_order.append(category)
        grouped[category].append((question, answer, remark))
    
    # We'll use the original appearance order of categories from the data
    for category in category_order:
        rows = grouped[category]

        elements.append(Spacer(1, 14))
        # Create section header with appropriate icon for each category
        if "Bedroom" in category:
            icon = "🛏️"
        elif "Bathroom" in category:
            icon = "🚿"
        elif "Kitchen" in category:
            icon = "🍳"
        elif "Living" in category:
            icon = "🛋️"
        elif "Dining" in category:
            icon = "🍽️"
        else:
            icon = "📌"
        
        elements.append(Paragraph(f"{icon} {category}", styles['SectionTitle']))
        elements.append(Spacer(1, 4))

        table_data = [["Question", "N/A", "Compliant", "Heads-Up", "Non-Compliant", "Remarks"]]

        for i, (question, answer, remark) in enumerate(rows):
            row = [Paragraph(question, wrap_style)]
            for choice, _ in MCQ_CHOICES:
                row.append("✔" if answer == choice else "")
            row.append(Paragraph(remark or "-", wrap_style))
            table_data.append(row)

        # Adjusted column widths to avoid overlapping
        table = Table(table_data, colWidths=[
            2.6 * inch, 0.7 * inch, 0.8 * inch, 0.9 * inch, 1.2 * inch, 2.2 * inch
        ])

        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e8f0f8")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#003366")),
            ('ALIGN', (1, 1), (-2, -1), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#003366")),
        ])

        for i in range(1, len(table_data)):
            bg = colors.whitesmoke if i % 2 == 0 else colors.white
            style.add('BACKGROUND', (0, i), (-1, i), bg)
            
            # Add subtle highlighting for non-compliant items
            if any(table_data[i][j] == "✔" for j in range(4, 5)):
                style.add('BACKGROUND', (0, i), (0, i), colors.HexColor("#fff8e1"))
                style.add('BACKGROUND', (4, i), (4, i), colors.HexColor("#ffebee"))
                style.add('TEXTCOLOR', (4, i), (4, i), colors.HexColor("#b71c1c"))

        table.setStyle(style)
        elements.append(table)

    doc.build(elements)
    return response

from django.http import HttpResponse
from openpyxl import Workbook
from .models import WalkthroughReport
from .models import CategoryCharField

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
    
    # Get all data from multiple models instead of single model
    all_data = get_verbose_data_from_models(report)
    
    # Get client name details
    client_first_name = report.user.first_name if report.user else ''
    client_last_name = report.user.last_name if report.user else ''
    client_name = f"{client_first_name} {client_last_name}".strip() or "N/A"
    
    # Format report date
    report_date = report.datetime.strftime('%Y-%m-%d') if report.datetime else 'N/A'
    
    # Get property information if available
    property_info = report.property.name if report.property.address and hasattr(report.property, 'name') else getattr(report.property.address, '__str__', lambda: 'N/A')()
    
    # Get report description (inspection note)
    inspection_note = getattr(report, 'description', '')
    response = HttpResponse(content_type='text/csv')
    filename = f"walkthrough_report_{report_id}.csv"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    writer = csv.writer(response)
    
    # Adding title with property name
    writer.writerow([property_info])
    writer.writerow([])  # Blank row for spacing
    
    # Report details
    writer.writerow(["Report Details:"])
    writer.writerow(["Client:", client_name])
    writer.writerow(["Date:", report_date])
    writer.writerow(["Inspection Note:", inspection_note])
    writer.writerow([])  # Blank row for spacing
    
    # Filter for only non-compliant items (similar to PDF function)
    non_compliant_data = [item for item in all_data if item[1] == "Non-Compliant"]
    
    # Section for non-compliant items
    writer.writerow(["Non-Compliant Items"])
    writer.writerow([])  # Blank row for spacing
    
    if not non_compliant_data:
        writer.writerow(["No non-compliant items found in this report."])
    else:
        # Group data by category while preserving order
        grouped = {}
        category_order = []
        
        for question, answer, remark, category in non_compliant_data:
            if category not in grouped:
                grouped[category] = []
                category_order.append(category)
            grouped[category].append((question, answer, remark))
        
        # Add data organized by category
        for category in category_order:
            rows = grouped[category]
            
            writer.writerow([category])
            writer.writerow(["Issue", "Status", "Remarks"])  # Headers for this category
            
            for question, answer, remark in rows:
                writer.writerow([question, "Non-Compliant", remark or "-"])
            
            writer.writerow([])  # Blank row to separate categories
    return response
# Creating Reports 

def all_reports_view(request):
    reports = WalkthroughReport.objects.all()
    return render(request, 'walkthrough/all_reports.html', {'reports': reports})

def my_reports_view(request):
    reports = WalkthroughReport.objects.all()
    return render(request, 'walkthrough/my_reports.html', {'reports': reports})

# def completed_reports_view(request):
#     reports = WalkthroughReport.objects.filter(status='Completed', item_status_check=True)
#     return render(request, 'walkthrough/completed_reports.html', {'reports': reports})

# def denied_reports_view(request):
#     reports = WalkthroughReport.objects.filter(status='Denied', item_status_check=True)
#     return render(request, 'walkthrough/denied_reports.html', {'reports': reports})


def update_walkthrough_report(request, report_id):
    report = get_object_or_404(WalkthroughReport, id=report_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        cost = request.POST.get('cost')

        if status:
            report.status = status
        if cost:
            try:
                report.cost = int(cost)
            except ValueError:
                pass

        report.save()
        return redirect('walkthroughreport:all_reports')

    return render(request, 'walkthrough/update_report.html', {
        'report': report,
        'base_template': 'cmbase.html'
    })

import copy
# def report_open_detail_view(request, pk):
#     report = get_object_or_404(WalkthroughReport, pk=pk)
    
#     # Create a modified version for the template
#     filtered_report = copy.deepcopy(report)
    
#     # Dynamically find all fields with prefix 'gie'
#     for field_name in dir(filtered_report):
#         # Check if it's a gie field but not a remarks field
#         if field_name.startswith('gie') and not field_name.endswith('_remarks'):
#             field_value = getattr(filtered_report, field_name, None)
#             # If the field exists and is not "Non-Compliant", set it to None
#             if field_value is not None and field_value != "Non-Compliant":
#                 setattr(filtered_report, field_name, None)
    
#     return render(request, 'walkthrough/report_open_detail.html', {'report': filtered_report})
import copy
from django.shortcuts import render, get_object_or_404
from .models import WalkthroughReport

def report_open_detail_view(request, pk):
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
    # Access the datetime field
   # Modify the datetime format to show only the date (Year-Month-Day)
    report_datetime = report.datetime.strftime('%Y-%m-%d') if report.datetime else 'No Datetime Available'
    report_property = report.property if report.property else 'Walkthrough Report'

    return render(request, 'walkthrough/report_open_detail.html', {'report': filtered_report,'client_first_name': client_first_name,
        'client_last_name': client_last_name,'report_datetime': report_datetime,'report_description':report_description,'report_property':report_property}) 


CATEGORY_MAP = {
    'gie': "General Items - Exterior",
    'gii': "General Items - Interior", 
    'garage': "Garage",
    'laundry': "Laundry / Mudroom",
    'kitchen': "Kitchen",
    'butlers': "Butlers",
    'breakfast': "Breakfast Area",
    'entry': "Entry / Voyer",
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
from .models import (
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
        })
    
    return inspection_items

def open_reports_view(request):
    reports = WalkthroughReport.objects.filter(
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
    
    return render(request, 'walkthrough/open_reports.html', {'reports': processed_reports})



def completed_reports_view(request):
    reports = WalkthroughReport.objects.filter(
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
    
    return render(request, 'walkthrough/completed_reports.html', {'reports': processed_reports})


def denied_reports_view(request):
    reports = WalkthroughReport.objects.filter(
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
    
    return render(request, 'walkthrough/denied_reports.html', {'reports': processed_reports})


# Add download thing for data of open report detail view --------------------------------------------------------------------- 
def open_export_pdf(request, report_id):
    import re
    
    report = WalkthroughReport.objects.get(pk=report_id)
    
    # Get all data but we'll filter for only non-compliant items later
    all_data = get_verbose_data(report)

    # Filter for only non-compliant items
    non_compliant_data = [item for item in all_data if item[1] == "Non-Compliant"]
    
    # Get client name details
    client_first_name = report.user.first_name if report.user else ''
    client_last_name = report.user.last_name if report.user else ''
    client_name = f"{client_first_name} {client_last_name}".strip() or "N/A"
    
    # Format report date
    report_date = report.datetime.strftime('%Y-%m-%d') if report.datetime else 'N/A'
    
    # Get property information if available
    property_info = report.property.name if report.property.address and hasattr(report.property, 'name') else getattr(report.property.address, '__str__', lambda: 'N/A')()
    
    # Get report description (inspection note)
    inspection_note = getattr(report, 'description', '')

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

    # Styles for different elements
    styles.add(ParagraphStyle(
        name='GreenTitle',
        fontSize=16,
        leading=18,
        textColor=colors.HexColor("#2e7d32"),
        fontName="Helvetica-Bold",
        alignment=1,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontSize=12,
        leading=15,
        spaceAfter=10,
        textColor=colors.HexColor("#003366"),
        fontName="Helvetica-Bold",
        borderPadding=(0, 0, 0, 4),
        borderWidth=0,
        borderColor=colors.HexColor("#003366"),
        borderRadius=None
    ))
    
    styles.add(ParagraphStyle(
        name='ReportInfo',
        fontSize=10,
        leading=12,
        spaceAfter=2,
        fontName="Helvetica",
    ))

    wrap_style = ParagraphStyle(
        name='wrapped',
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        wordWrap='CJK',
    )

    # Main heading with property name
    elements.append(Paragraph(f"🏠 {property_info}", styles['GreenTitle']))

    # Underline
    elements.append(Table([[""]], colWidths=[6.3 * inch], style=[
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor("#2e7d32"))],
    ))
    elements.append(Spacer(1, 12))
    
    # Report details section
    elements.append(Paragraph("Report Details:", styles['SectionTitle']))
    elements.append(Paragraph(f"<b>Client:</b> {client_name}", styles['ReportInfo']))
    elements.append(Paragraph(f"<b>Date:</b> {report_date}", styles['ReportInfo']))
    elements.append(Paragraph(f"<b>Inspection Note:</b> {inspection_note}", styles['ReportInfo']))
    
    elements.append(Spacer(1, 20))
    
    # Add non-compliant items section title
    elements.append(Paragraph("⚠️ Non-Compliant Items", styles['SectionTitle']))
    elements.append(Spacer(1, 10))

    if not non_compliant_data:
        elements.append(Paragraph("No non-compliant items found in this report.", styles['ReportInfo']))
    else:
        # Grouping data by exact category name while preserving order
        grouped = {}
        category_order = []
        
        for question, answer, remark, category in non_compliant_data:
            if category not in grouped:
                grouped[category] = []
                category_order.append(category)
            grouped[category].append((question, answer, remark))
        
        for category in category_order:
            rows = grouped[category]

            elements.append(Spacer(1, 14))
            
            # Create section header with appropriate icon for each category
            if "Bedroom" in category:
                icon = "🛏️"
            elif "Bathroom" in category:
                icon = "🚿"
            elif "Kitchen" in category:
                icon = "🍳"
            elif "Living" in category:
                icon = "🛋️"
            elif "Dining" in category:
                icon = "🍽️"
            else:
                icon = "📌"
            
            elements.append(Paragraph(f"{icon} {category}", styles['SectionTitle']))
            elements.append(Spacer(1, 4))

            table_data = [["Issue", "Status", "Remarks"]]

            for question, answer, remark in rows:
                table_data.append([
                    Paragraph(question, wrap_style),
                    "Non-Compliant",
                    Paragraph(remark or "-", wrap_style)
                ])

            # Adjusted column widths
            table = Table(table_data, colWidths=[3.0 * inch, 1.0 * inch, 3.4 * inch])

            style = TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e8f0f8")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#003366")),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # Center the "Status" column
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#003366")),
            ])

            # Add red background to all non-compliant status cells
            for i in range(1, len(table_data)):
                style.add('BACKGROUND', (1, i), (1, i), colors.HexColor("#ffebee"))  # Light red background
                style.add('TEXTCOLOR', (1, i), (1, i), colors.HexColor("#b71c1c"))   # Dark red text

            for i in range(1, len(table_data)):
                bg = colors.whitesmoke if i % 2 == 0 else colors.white
                style.add('BACKGROUND', (0, i), (0, i), bg)
                style.add('BACKGROUND', (2, i), (2, i), bg)

            table.setStyle(style)
            elements.append(table)

    doc.build(elements)
    return response
    
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
def report_detail_view(request, pk):
    report = get_object_or_404(WalkthroughReport, pk=pk)
    
    # All related models to check (same as in open_reports_view)
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
    
    # Create a context dictionary with the report and all related model instances
    context = {'report': report}
    
    # Add each related model instance to the context
    for model_class, relation_name in related_models:
        try:
            # Get the related model instance
            model_instance = getattr(report, relation_name, None)
            context[relation_name] = model_instance
        except Exception as e:
            # Handle cases where relation doesn't exist
            context[relation_name] = None
    
    # Add verbose names for all model fields
    def get_verbose_names():
        verbose_names = {}
        for model_class, relation_name in related_models:
            if context.get(relation_name):
                for field in model_class._meta.fields:
                    if hasattr(field, 'verbose_name') and field.name != 'id':
                        verbose_names[f"{field.name}_verbose"] = field.verbose_name
        return verbose_names
    
    context.update(get_verbose_names())
    print(f"Bedroom9: {getattr(report, 'bedroom9', 'NOT FOUND')}")
    return render(request, 'walkthrough/report_detail.html', context)
# Report Updates ----------------------------------------------------------------------
from django.http import JsonResponse
from .models import WalkthroughReport
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



@csrf_exempt
def update_cost_ajax(request, report_id):
    if request.method == 'POST':
        cost = request.POST.get('cost')
        cost_notes = request.POST.get('cost_notes')
        report = WalkthroughReport.objects.get(id=report_id)
        report.cost = int(cost)
        report.cost_notes = cost_notes
        report.save()
        return JsonResponse({'success': True, 'new_cost': report.cost, 'new_notes': report.cost_notes})
    return JsonResponse({'success': False})

@csrf_exempt
def update_client_approval(request, report_id):
    if request.method == 'POST':
        status = request.POST.get('approval')
        if status not in ['Approved', 'Denied']:
            return JsonResponse({'success': False})
        try:
            report = WalkthroughReport.objects.get(id=report_id)
            report.client_approval = status
            report.save()
            return JsonResponse({'success': True, 'new_status': report.client_approval})
        except:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import WalkthroughReport
from datetime import datetime
@csrf_exempt
def update_status(request, report_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        date_str = request.POST.get('date')
        remarks = request.POST.get('remarks', '')

        if new_status not in ['Completed', 'Denied'] or not date_str:
            return JsonResponse({'success': False})

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            report = WalkthroughReport.objects.get(id=report_id)
            report.status = new_status
            report.completation_denied_date = date_obj
            report.status_remarks = remarks
            report.save()
            return JsonResponse({
                'success': True,
                'new_status': new_status,
                'new_date': str(date_obj)
            })
        except:
            return JsonResponse({'success': False})

    return JsonResponse({'success': False})


from django.http import JsonResponse



# New format things starts --------------------------------------------------------------------------------------------
import json
@csrf_exempt
def update_report_field_cost(request, report_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        category = data.get('category')
        question = data.get('question')
        amount = data.get('amount')
        calculation_note = data.get('calculation_note')

        print(f"Received data - Category: '{category}', Question: '{question}', Amount: {amount}")
        
        try:
            report = WalkthroughReport.objects.get(id=report_id)
            print(f"Found report: {report.id}")
            
            # Model mapping based on category
            model_mapping = {
                'General Items - Exterior': ('general_items_exterior', GeneralItemsExterior),
                'General Items - Interior': ('general_items_interior', GeneralItemsInterior),
                'Garage': ('garage', Garage),
                'Laundry / Mudroom': ('laundry', Laundry),
                'Kitchen': ('kitchen', Kitchen),
                'Butlers': ('butlers', Butlers),
                'Breakfast Area': ('breakfastarea', BreakfastArea),
                'Entry / Foyer': ('entryfoyer', EntryFoyer),
                'Great Room / Family Room': ('greatroom', GreatRoom),
                'Dining Room / Area': ('diningroom', DiningRoom),
                'Closets - Main Level': ('closetsmainlevel', ClosetsMainLevel),
                'Closets - Upper Level': ('closetsupperlevel', ClosetsUpperLevel),
                'Hallways - Main Level': ('hallwaysmainlevel', HallwaysMainLevel),
                'Hallways - Upper Level': ('hallwaysupperlevel', HallwaysUpperLevel),
                'Bedroom 1 (Master Bedroom)': ('bedroom1', Bedroom1),
                'Bedroom 2': ('bedroom2', Bedroom2),
                'Bedroom 3': ('bedroom3', Bedroom3),
                'Bedroom 4': ('bedroom4', Bedroom4),
                'Bedroom 5': ('bedroom5', Bedroom5),
                'Bedroom 6': ('bedroom6', Bedroom6),
                'Bedroom 7': ('bedroom7', Bedroom7),
                'Bedroom 8': ('bedroom8', Bedroom8),
                'Bedroom 9': ('bedroom9', Bedroom9),
                'Bedroom 10': ('bedroom10', Bedroom10),
                'Bathroom 1 (Master Bath)': ('bathroom1', Bathroom1),
                'Bathroom 2': ('bathroom2', Bathroom2),
                'Bathroom 3': ('bathroom3', Bathroom3),
                'Bathroom 4': ('bathroom4', Bathroom4),
                'Bathroom 5': ('bathroom5', Bathroom5),
                'Bathroom 6': ('bathroom6', Bathroom6),
                'Bathroom 7': ('bathroom7', Bathroom7),
                'Bathroom 8': ('bathroom8', Bathroom8),
                'Bathroom 9': ('bathroom9', Bathroom9),
                'Bathroom 10': ('bathroom10', Bathroom10),
                'Bathroom 11': ('bathroom11', Bathroom11),
                'Bathroom 12': ('bathroom12', Bathroom12),
                'Gym': ('gym', Gym),
                'Theatre / Music Room': ('theatremusicroom', TheatreMusicRoom),
                'Guest House - Sleeping / Living': ('guesthousesleepingliving', GuestHouseSleepingLiving),
                'Guest House - Bathroom': ('guesthousebathroom', GuestHouseBathroom),
            }
            
            if category in model_mapping:
                print(f"Category '{category}' found in mapping")
                related_name, model_class = model_mapping[category]
                print(f"Using model: {model_class.__name__}")
                
                # Get or create the related model instance
                related_instance, created = model_class.objects.get_or_create(
                    walkthrough_report=report
                )
                print(f"Got model instance, created: {created}")
                
                # Find the field by matching verbose_name with the question
                field_found = False
                print(f"Looking for field with verbose_name: '{question}'")
                
                for field in related_instance._meta.get_fields():
                    if hasattr(field, 'verbose_name'):
                        print(f"Checking field '{field.name}' with verbose_name: '{field.verbose_name}'")
                        if field.verbose_name == question:
                            print(f"MATCH FOUND! Field: {field.name}")
                            base_field_name = field.name
                            amount_field = f"{base_field_name}_amount"
                            note_field = f"{base_field_name}_calculation_note"
                            
                            print(f"Looking for amount field: {amount_field}")
                            print(f"Looking for note field: {note_field}")
                            
                            # Update the amount field
                            if hasattr(related_instance, amount_field):
                                print(f"Setting {amount_field} = {amount}")
                                setattr(related_instance, amount_field, amount)
                            else:
                                print(f"Amount field {amount_field} not found")
                            
                            # Update the calculation note field
                            if hasattr(related_instance, note_field):
                                print(f"Setting {note_field} = {calculation_note}")
                                setattr(related_instance, note_field, calculation_note)
                            else:
                                print(f"Note field {note_field} not found")
                            
                            related_instance.save()
                            print("Instance saved successfully")
                            field_found = True
                            break
                
                if field_found:
                    print("Returning success")
                    return JsonResponse({'success': True})
                else:
                    print(f"No field found with verbose_name: '{question}' in category: {category}")
                    # Debug: show all verbose names
                    verbose_names = []
                    for field in related_instance._meta.get_fields():
                        if hasattr(field, 'verbose_name'):
                            verbose_names.append(f"'{field.verbose_name}'")
                    print(f"Available verbose names: {verbose_names}")
            else:
                print(f"Category '{category}' not found in model_mapping")
            
        except Exception as e:
            print("Update failed:", e)
            print(f"Category: {category}")
            print(f"Question: '{question}'")
            print(f"Amount: {amount}")
            print(f"Calculation note: {calculation_note}")
            import traceback
            traceback.print_exc()
    
    return JsonResponse({'success': False})

@csrf_exempt
def update_client_approval(request, report_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        field_name = data.get('field_name')
        client_approval = data.get('client_approval')
        category = data.get('category')
        
        print(f"Received approval update - Category: '{category}', Field: '{field_name}', Approval: {client_approval}")

        try:
            report = WalkthroughReport.objects.get(id=report_id)
            print(f"Found report: {report.id}")
            
            # Model mapping based on category
            model_mapping = {
                'General Items - Exterior': ('general_items_exterior', GeneralItemsExterior),
                'General Items - Interior': ('general_items_interior', GeneralItemsInterior),
                'Garage': ('garage', Garage),
                'Laundry / Mudroom': ('laundry', Laundry),
                'Kitchen': ('kitchen', Kitchen),
                'Butlers': ('butlers', Butlers),
                'Breakfast Area': ('breakfastarea', BreakfastArea),
                'Entry / Foyer': ('entryfoyer', EntryFoyer),
                'Great Room / Family Room': ('greatroom', GreatRoom),
                'Dining Room / Area': ('diningroom', DiningRoom),
                'Closets - Main Level': ('closetsmainlevel', ClosetsMainLevel),
                'Closets - Upper Level': ('closetsupperlevel', ClosetsUpperLevel),
                'Hallways - Main Level': ('hallwaysmainlevel', HallwaysMainLevel),
                'Hallways - Upper Level': ('hallwaysupperlevel', HallwaysUpperLevel),
                'Bedroom 1 (Master Bedroom)': ('bedroom1', Bedroom1),
                'Bedroom 2': ('bedroom2', Bedroom2),
                'Bedroom 3': ('bedroom3', Bedroom3),
                'Bedroom 4': ('bedroom4', Bedroom4),
                'Bedroom 5': ('bedroom5', Bedroom5),
                'Bedroom 6': ('bedroom6', Bedroom6),
                'Bedroom 7': ('bedroom7', Bedroom7),
                'Bedroom 8': ('bedroom8', Bedroom8),
                'Bedroom 9': ('bedroom9', Bedroom9),
                'Bedroom 10': ('bedroom10', Bedroom10),
                'Bathroom 1 (Master Bath)': ('bathroom1', Bathroom1),
                'Bathroom 2': ('bathroom2', Bathroom2),
                'Bathroom 3': ('bathroom3', Bathroom3),
                'Bathroom 4': ('bathroom4', Bathroom4),
                'Bathroom 5': ('bathroom5', Bathroom5),
                'Bathroom 6': ('bathroom6', Bathroom6),
                'Bathroom 7': ('bathroom7', Bathroom7),
                'Bathroom 8': ('bathroom8', Bathroom8),
                'Bathroom 9': ('bathroom9', Bathroom9),
                'Bathroom 10': ('bathroom10', Bathroom10),
                'Bathroom 11': ('bathroom11', Bathroom11),
                'Bathroom 12': ('bathroom12', Bathroom12),
                'Gym': ('gym', Gym),
                'Theatre / Music Room': ('theatremusicroom', TheatreMusicRoom),
                'Guest House - Sleeping / Living': ('guesthousesleepingliving', GuestHouseSleepingLiving),
                'Guest House - Bathroom': ('guesthousebathroom', GuestHouseBathroom),
            }
            
            if category in model_mapping:
                print(f"Category '{category}' found in mapping")
                related_name, model_class = model_mapping[category]
                print(f"Using model: {model_class.__name__}")
                
                # Get or create the related model instance
                related_instance, created = model_class.objects.get_or_create(
                    walkthrough_report=report
                )
                print(f"Got model instance, created: {created}")
                
                # Update the client approval field
                approval_field = f"{field_name}_client_approval"
                print(f"Looking for approval field: {approval_field}")
                
                if hasattr(related_instance, approval_field):
                    print(f"Setting {approval_field} = {client_approval}")
                    setattr(related_instance, approval_field, client_approval)
                    related_instance.save()
                    print("Instance saved successfully")
                    return JsonResponse({'status': 'success'})
                else:
                    print(f"Approval field {approval_field} not found")
                    return JsonResponse({'status': 'error', 'message': f'Field {approval_field} not found'}, status=400)
            else:
                print(f"Category '{category}' not found in model_mapping")
                return JsonResponse({'status': 'error', 'message': f'Category {category} not found'}, status=400)
                     
        except Exception as e:
            print("Update failed:", e)
            import traceback
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
from datetime import datetime
from django.utils.dateparse import parse_datetime

@csrf_exempt
def update_field_status_ajax(request, report_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            field_name = data.get('field_name')
            update_status = data.get('new_status')
            update_date = data.get('datetime')
            update_remarks = data.get('remarks')
            category = data.get('category')

            print(f"Received status update - Category: '{category}', Field: '{field_name}', Status: {update_status}")

            report = WalkthroughReport.objects.get(id=report_id)
            print(f"Found report: {report.id}")
            
            # Model mapping based on category
            model_mapping = {
                'General Items - Exterior': ('general_items_exterior', GeneralItemsExterior),
                'General Items - Interior': ('general_items_interior', GeneralItemsInterior),
                'Garage': ('garage', Garage),
                'Laundry / Mudroom': ('laundry', Laundry),
                'Kitchen': ('kitchen', Kitchen),
                'Butlers': ('butlers', Butlers),
                'Breakfast Area': ('breakfastarea', BreakfastArea),
                'Entry / Foyer': ('entryfoyer', EntryFoyer),
                'Great Room / Family Room': ('greatroom', GreatRoom),
                'Dining Room / Area': ('diningroom', DiningRoom),
                'Closets - Main Level': ('closetsmainlevel', ClosetsMainLevel),
                'Closets - Upper Level': ('closetsupperlevel', ClosetsUpperLevel),
                'Hallways - Main Level': ('hallwaysmainlevel', HallwaysMainLevel),
                'Hallways - Upper Level': ('hallwaysupperlevel', HallwaysUpperLevel),
                'Bedroom 1 (Master Bedroom)': ('bedroom1', Bedroom1),
                'Bedroom 2': ('bedroom2', Bedroom2),
                'Bedroom 3': ('bedroom3', Bedroom3),
                'Bedroom 4': ('bedroom4', Bedroom4),
                'Bedroom 5': ('bedroom5', Bedroom5),
                'Bedroom 6': ('bedroom6', Bedroom6),
                'Bedroom 7': ('bedroom7', Bedroom7),
                'Bedroom 8': ('bedroom8', Bedroom8),
                'Bedroom 9': ('bedroom9', Bedroom9),
                'Bedroom 10': ('bedroom10', Bedroom10),
                'Bathroom 1 (Master Bath)': ('bathroom1', Bathroom1),
                'Bathroom 2': ('bathroom2', Bathroom2),
                'Bathroom 3': ('bathroom3', Bathroom3),
                'Bathroom 4': ('bathroom4', Bathroom4),
                'Bathroom 5': ('bathroom5', Bathroom5),
                'Bathroom 6': ('bathroom6', Bathroom6),
                'Bathroom 7': ('bathroom7', Bathroom7),
                'Bathroom 8': ('bathroom8', Bathroom8),
                'Bathroom 9': ('bathroom9', Bathroom9),
                'Bathroom 10': ('bathroom10', Bathroom10),
                'Bathroom 11': ('bathroom11', Bathroom11),
                'Bathroom 12': ('bathroom12', Bathroom12),
                'Gym': ('gym', Gym),
                'Theatre / Music Room': ('theatremusicroom', TheatreMusicRoom),
                'Guest House - Sleeping / Living': ('guesthousesleepingliving', GuestHouseSleepingLiving),
                'Guest House - Bathroom': ('guesthousebathroom', GuestHouseBathroom),
            }
            
            if category in model_mapping:
                print(f"Category '{category}' found in mapping")
                related_name, model_class = model_mapping[category]
                print(f"Using model: {model_class.__name__}")
                
                # Get or create the related model instance
                related_instance, created = model_class.objects.get_or_create(
                    walkthrough_report=report
                )
                print(f"Got model instance, created: {created}")
                
                # Update status field
                status_field = f'{field_name}_udpate_status'
                print(f"Looking for status field: {status_field}")
                if hasattr(related_instance, status_field):
                    print(f"Setting {status_field} = {update_status}")
                    setattr(related_instance, status_field, update_status)
                else:
                    print(f"Status field {status_field} not found")
                
                # Update date field
                if update_date:
                    from datetime import datetime
                    date_obj = datetime.strptime(update_date, '%Y-%m-%d').date()
                    date_field = f'{field_name}_update_date'
                    print(f"Looking for date field: {date_field}")
                    if hasattr(related_instance, date_field):
                        print(f"Setting {date_field} = {date_obj}")
                        setattr(related_instance, date_field, date_obj)
                    else:
                        print(f"Date field {date_field} not found")
                
                # Update remarks field
                remarks_field = f'{field_name}_update_remarks'
                print(f"Looking for remarks field: {remarks_field}")
                if hasattr(related_instance, remarks_field):
                    print(f"Setting {remarks_field} = {update_remarks}")
                    setattr(related_instance, remarks_field, update_remarks)
                else:
                    print(f"Remarks field {remarks_field} not found")
                
                related_instance.save()
                print("Instance saved successfully")
                return JsonResponse({'success': True})
            else:
                print(f"Category '{category}' not found in model_mapping")
                return JsonResponse({'success': False, 'error': f'Category {category} not found'})
            
        except Exception as e:
            print(f"Update failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["POST"])
def bulk_update_status(request):
    try:
        data = json.loads(request.body)
        report_ids = data.get('report_ids', [])
        status = data.get('status', 'Completed')
        
        if not report_ids:
            return JsonResponse({'success': False, 'error': 'No report IDs provided'})
        
        # Update all reports with the given IDs
        updated_count = WalkthroughReport.objects.filter(
            id__in=report_ids
        ).update(status=status)
        
        return JsonResponse({
            'success': True, 
            'updated_count': updated_count,
            'message': f'{updated_count} reports updated successfully'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})