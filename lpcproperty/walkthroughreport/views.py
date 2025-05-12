from django.shortcuts import render

# Create your views here.
# views.py

from django.shortcuts import render
from .models import WalkthroughReport
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

CATEGORY_LABELS = {
    "GIE": "General Items - Exterior",
    "GII": "General Items - Interior",
    "GUESTHOUSEBATH": "Guest House Bath",
    "THEATER": "Theatre / Music Room",
    # Add more mappings as needed
}

def get_verbose_data(report):
    data = []
    for field in report._meta.fields:
        name = field.name
        if name[-1:].isdigit() and not name.endswith('_remarks'):
            answer = getattr(report, name)
            remark = getattr(report, f"{name}_remarks", '')

            if answer:
                field_instance = field
                verbose = field_instance.verbose_name or name.replace('_', ' ').capitalize()
                
                # Get the category directly from the field
                if hasattr(field_instance, 'category'):
                    category = field_instance.category
                else:
                    # If no category attribute exists, extract from field name
                    # This is a more robust way to handle bathroom fields
                    if 'bathroom' in name:
                        # Extract bathroom number (bathroom1, bathroom2, etc.)
                        bathroom_match = re.search(r'bathroom(\d+)', name)
                        if bathroom_match:
                            bathroom_num = bathroom_match.group(1)
                            category = f"Bathroom {bathroom_num}"
                        else:
                            category = "Bathroom"
                    else:
                        # Fall back to the original method for other fields
                        prefix = ''.join(filter(str.isalpha, name)).upper()
                        category = CATEGORY_LABELS.get(prefix, prefix)
                
                data.append((verbose, answer, remark, category))
    return data

def export_pdf(request, report_id):
    import re
    
    report = WalkthroughReport.objects.get(pk=report_id)
    
    # Get all data (no filtering)
    data = get_verbose_data(report)
    
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
        
        elements.append(Paragraph(f"{icon} {category}", styles['SectionTitle']))  # Use the full category name
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
            2.6 * inch, 0.7 * inch, 0.8 * inch, 0.9 * inch, 1.2 * inch, 2.2 * inch  # Wider "Non-Compliant" and "Remarks"
        ])

        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e8f0f8")),  # Lighter header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#003366")),
            ('ALIGN', (1, 1), (-2, -1), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically center all cell content
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#003366")),  # Add border around table
        ])

        for i in range(1, len(table_data)):
            bg = colors.whitesmoke if i % 2 == 0 else colors.white
            style.add('BACKGROUND', (0, i), (-1, i), bg)
            
            # Add subtle highlighting for non-compliant items
            if any(table_data[i][j] == "✔" for j in range(4, 5)):  # Check Non-Compliant column
                style.add('BACKGROUND', (0, i), (0, i), colors.HexColor("#fff8e1"))  # Light yellow for question
                style.add('BACKGROUND', (4, i), (4, i), colors.HexColor("#ffebee"))  # Light red for checkmark
                style.add('TEXTCOLOR', (4, i), (4, i), colors.HexColor("#b71c1c"))   # Dark red text

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
    
    # Get all data
    all_data = get_verbose_data(report)
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
from django.shortcuts import render, get_object_or_404
def report_detail_view(request, pk):
    report = get_object_or_404(WalkthroughReport, pk=pk)
    return render(request, 'walkthrough/report_detail.html', {'report': report})

def all_reports_view(request):
    reports = WalkthroughReport.objects.all()
    return render(request, 'walkthrough/all_reports.html', {'reports': reports})

def my_reports_view(request):
    reports = WalkthroughReport.objects.all()
    return render(request, 'walkthrough/my_reports.html', {'reports': reports})

def completed_reports_view(request):
    reports = WalkthroughReport.objects.filter(status='Completed')
    return render(request, 'walkthrough/completed_reports.html', {'reports': reports})

def denied_reports_view(request):
    reports = WalkthroughReport.objects.filter(status='Denied')
    return render(request, 'walkthrough/denied_reports.html', {'reports': reports})


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

from django.db.models import Q
def open_reports_view(request):
    reports = WalkthroughReport.objects.exclude(Q(status='Completed') | Q(status='Denied'))
    return render(request, 'walkthrough/open_reports.html', {'reports': reports})


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
    