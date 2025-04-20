from django.shortcuts import render

# Create your views here.
# def cm_login(request):
#     return render(request, 'clientmanager/cm_login.html')

from django.shortcuts import render, redirect
from mainapp.models import ClientManagers
from django.contrib import messages


def client_manager_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = ClientManagers.objects.get(username=username)
            if user.check_password(password):
                request.session.flush()  # clear any previous session
                request.session['manager_id'] = user.id  # ✅ correct session key
                return redirect('clientmanager:client_dashboard')  # use your actual dashboard route
            else:
                messages.error(request, 'Invalid password')
        except ClientManagers.DoesNotExist:
            messages.error(request, 'User not found')

    return render(request, 'clientmanager/login.html')



from django.shortcuts import render

def client_dashboard_view(request):
    manager_id = request.session.get('manager_id')  # ✅ not client_id
    if not manager_id:
        return redirect('clientmanager:client_login')

    return render(request, 'clientmanager/dashboard.html')

def client_logout_view(request):
    request.session.flush()
    return redirect('clientmanager:client_login')


# Building Property  ---------------------------------------------------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from propertydetails.models import PropertyManagement
from django.contrib import messages

def get_client_manager_id(request):
    return request.session.get('client_id')

# def client_list_page(request):
#     clients = Client.objects.all()
#     return render(request, 'clientmanager/client/client_list_page.html', {'clients': clients})
def property_list_view(request):
    manager_id = request.session.get('manager_id') 
    clients = Client.objects.all()
    properties = PropertyManagement.objects.filter(client_manager_id=manager_id)
    return render(request, 'clientmanager/property/list.html', {'properties': properties,'clients': clients})


def property_detail_view(request, pk):
    manager_id = request.session.get('manager_id') 
    prop = get_object_or_404(PropertyManagement, pk=pk, client_manager_id=manager_id)
    return render(request, 'clientmanager/property/detail.html', {'property': prop})

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
from propertydetails.models import PropertyManagement

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.conf import settings
import os
from django.shortcuts import get_object_or_404

def link_callback(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

def export_property_pdf(request, pk):
    prop = get_object_or_404(PropertyManagement, pk=pk)
    template_path = 'clientmanager/property/pdf_template.html'
    context = {'property': prop}
    html = render_to_string(template_path, context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="property_{prop.pk}.pdf"'

    pisa.CreatePDF(
        html,
        dest=response,
        link_callback=link_callback  # This fixes the image path issue
    )

    return response




from django.shortcuts import render, redirect
from propertydetails.models import PropertyManagement, Floor, Room
from mainapp.models import Client 
from django.db import transaction

def property_create_view(request):
    clients = Client.objects.all()
    managers = ClientManagers.objects.all()

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Get client_id if selected
                client_id = request.POST.get('client_id')
                
                # If no existing client selected, try creating a new one
                if not client_id:
                    new_first_name = request.POST.get('new_first_name', '')
                    new_last_name = request.POST.get('new_last_name', '')
                    new_username = request.POST.get('new_username', '')
                    new_email = request.POST.get('new_email', '')
                    new_password = request.POST.get('new_password', '')
                    new_phone = request.POST.get('new_phone', '')

                    if not all([new_first_name, new_last_name, new_username, new_email, new_password]):
                        raise ValueError("Fill all required fields for new client")

                    new_client = Client.objects.create(
                        first_name=new_first_name,
                        last_name=new_last_name,
                        username=new_username,
                        email=new_email,
                        password=new_password,  # storing plain for now
                        phone_number=new_phone
                    )
                    client_id = new_client.id

                # Validate required fields
                client_manager_id = request.POST.get('client_manager_id')
                address = request.POST.get('address')
                if not all([client_id, client_manager_id, address]):
                    raise ValueError("Client Manager and Address are required")

                # Create the Property
                prop = PropertyManagement.objects.create(
                    client_id=client_id,
                    client_manager_id=client_manager_id,
                    address=address,
                    size_of_home=request.POST.get('size_of_home', ''),
                    number_of_stories=request.POST.get('number_of_stories', ''),
                    construction_type=request.POST.get('construction_type', ''),
                    year_built=request.POST.get('year_built', ''),
                    has_pool='has_pool' in request.POST,
                    gated_community='gated_community' in request.POST,
                    impact_windows='impact_windows' in request.POST,
                    has_hoa='has_hoa' in request.POST,
                    gated_property='gated_property' in request.POST,
                    preferred_contact_method=request.POST.get('preferred_contact_method', 'email'),
                )

                # Loop through each floor and room
                floor_count = len([k for k in request.POST if k.startswith('floor_name_')])
                for i in range(1, floor_count + 1):
                    floor_name = request.POST.get(f'floor_name_{i}')
                    if not floor_name:
                        continue
                    floor = Floor.objects.create(property=prop, floor_name=floor_name)

                    room_count = len([k for k in request.POST if k.startswith(f'room_name_{i}_')])
                    for j in range(1, room_count + 1):
                        room_name = request.POST.get(f'room_name_{i}_{j}')
                        room_size = request.POST.get(f'room_size_{i}_{j}')
                        room_image = request.FILES.get(f'room_image_{i}_{j}')
                        if room_name:
                            Room.objects.create(
                                floor=floor,
                                room_name=room_name,
                                room_size=room_size,
                                room_image=room_image
                            )

                return redirect('clientmanager:property_list')

        except Exception as e:
            print("Error occurred:", str(e))  # Shows error in terminal
            return render(request, 'clientmanager/property/create.html', {
                'clients': clients,
                'managers': managers,
                'error_message': str(e)
            })

    return render(request, 'clientmanager/property/create.html', {
        'clients': clients,
        'managers': managers
    })

def property_update_view(request, pk):
    manager_id = request.session.get('manager_id') 
    prop = get_object_or_404(PropertyManagement, pk=pk, client_manager_id=manager_id)
    client = prop.client  # assumes there's a ForeignKey to Client

    if request.method == 'POST':
        # Property fields
        prop.address = request.POST['address']
        prop.size_of_home = request.POST.get('size_of_home', '')
        prop.number_of_stories = request.POST.get('number_of_stories', '')
        prop.construction_type = request.POST.get('construction_type', '')
        prop.year_built = request.POST.get('year_built', '')
        prop.has_pool = 'has_pool' in request.POST
        prop.gated_community = 'gated_community' in request.POST
        prop.impact_windows = 'impact_windows' in request.POST
        prop.has_hoa = 'has_hoa' in request.POST
        prop.gated_property = 'gated_property' in request.POST
        prop.preferred_contact_method = request.POST.get('preferred_contact_method', 'email')
        prop.save()

        # Update Client info
        client.first_name = request.POST.get('client_first_name', '')
        client.last_name = request.POST.get('client_last_name', '')
        client.username = request.POST.get('client_username', '')
        client.email = request.POST.get('client_email', '')
        client.address = request.POST.get('client_address', '')
        client.city = request.POST.get('client_city', '')
        client.state = request.POST.get('client_state', '')
        client.zipcode = request.POST.get('client_zipcode', '')
        client.phone_number = request.POST.get('client_phone_number', '')
        client.preferred_contact_method = request.POST.get('client_preferred_contact_method', 'email')

        # Contact Person 1
        client.contact1_name = request.POST.get('contact1_name', '')
        client.contact1_email = request.POST.get('contact1_email', '')
        client.contact1_phone = request.POST.get('contact1_phone', '')
        client.contact1_preferred = request.POST.get('contact1_preferred', '')

        # Contact Person 2
        client.contact2_name = request.POST.get('contact2_name', '')
        client.contact2_email = request.POST.get('contact2_email', '')
        client.contact2_phone = request.POST.get('contact2_phone', '')
        client.contact2_preferred = request.POST.get('contact2_preferred', '')

        # Contact Person 3
        client.contact3_name = request.POST.get('contact3_name', '')
        client.contact3_email = request.POST.get('contact3_email', '')
        client.contact3_phone = request.POST.get('contact3_phone', '')
        client.contact3_preferred = request.POST.get('contact3_preferred', '')

        client.save()

        # Process Floors and Rooms
        existing_floors = {f"floor_name_{i}": floor for i, floor in enumerate(prop.floors.all(), start=1)}

        i = 1
        while True:
            floor_key = f'floor_name_{i}'
            if floor_key not in request.POST:
                break

            floor_name = request.POST.get(floor_key)

            # Reuse or create floor
            floor = existing_floors.get(floor_key)
            if floor:
                floor.floor_name = floor_name
                floor.save()
            else:
                floor = Floor.objects.create(property=prop, floor_name=floor_name)

            j = 1
            while True:
                room_name_key = f'room_name_{i}_{j}'
                room_size_key = f'room_size_{i}_{j}'
                room_image_key = f'room_image_{i}_{j}'

                if room_name_key not in request.POST:
                    break

                room_name = request.POST.get(room_name_key)
                room_size = request.POST.get(room_size_key)
                room_image = request.FILES.get(room_image_key)

                # Try to reuse an existing room or create a new one
                if j <= floor.rooms.count():
                    room = floor.rooms.all()[j-1]
                    room.room_name = room_name
                    room.room_size = room_size
                    if room_image:
                        room.room_image = room_image
                    room.save()
                else:
                    Room.objects.create(
                        floor=floor,
                        room_name=room_name,
                        room_size=room_size,
                        room_image=room_image
                    )
                j += 1
            i += 1

        # Floors & Rooms update logic here (same as before)

        # ... floors/rooms logic remains unchanged ...

        return redirect('clientmanager:property_list')

    floors = prop.floors.prefetch_related('rooms').all()
    return render(request, 'clientmanager/property/edit.html', {
        'property': prop,
        'floors': floors,
        'client': client,
    })


# def property_update_view(request, pk):
#     manager_id = request.session.get('manager_id') 
#     prop = get_object_or_404(PropertyManagement, pk=pk, client_manager_id=manager_id)

#     if request.method == 'POST':
#         # Update Property fields
#         prop.address = request.POST['address']
#         prop.size_of_home = request.POST.get('size_of_home', '')
#         prop.number_of_stories = request.POST.get('number_of_stories', '')
#         prop.construction_type = request.POST.get('construction_type', '')
#         prop.year_built = request.POST.get('year_built', '')
#         prop.has_pool = 'has_pool' in request.POST
#         prop.gated_community = 'gated_community' in request.POST
#         prop.impact_windows = 'impact_windows' in request.POST
#         prop.has_hoa = 'has_hoa' in request.POST
#         prop.gated_property = 'gated_property' in request.POST
#         prop.preferred_contact_method = request.POST.get('preferred_contact_method', 'email')
#         prop.save()

#         # Process Floors and Rooms
#         existing_floors = {f"floor_name_{i}": floor for i, floor in enumerate(prop.floors.all(), start=1)}

#         i = 1
#         while True:
#             floor_key = f'floor_name_{i}'
#             if floor_key not in request.POST:
#                 break

#             floor_name = request.POST.get(floor_key)

#             # Reuse or create floor
#             floor = existing_floors.get(floor_key)
#             if floor:
#                 floor.floor_name = floor_name
#                 floor.save()
#             else:
#                 floor = Floor.objects.create(property=prop, floor_name=floor_name)

#             j = 1
#             while True:
#                 room_name_key = f'room_name_{i}_{j}'
#                 room_size_key = f'room_size_{i}_{j}'
#                 room_image_key = f'room_image_{i}_{j}'

#                 if room_name_key not in request.POST:
#                     break

#                 room_name = request.POST.get(room_name_key)
#                 room_size = request.POST.get(room_size_key)
#                 room_image = request.FILES.get(room_image_key)

#                 # Try to reuse an existing room or create a new one
#                 if j <= floor.rooms.count():
#                     room = floor.rooms.all()[j-1]
#                     room.room_name = room_name
#                     room.room_size = room_size
#                     if room_image:
#                         room.room_image = room_image
#                     room.save()
#                 else:
#                     Room.objects.create(
#                         floor=floor,
#                         room_name=room_name,
#                         room_size=room_size,
#                         room_image=room_image
#                     )
#                 j += 1
#             i += 1

#         return redirect('clientmanager:property_list')

#     floors = prop.floors.prefetch_related('rooms').all()
#     return render(request, 'clientmanager/property/edit.html', {
#         'property': prop,
#         'floors': floors
#     })


def property_delete_view(request, pk):
    # manager_id = request.session.get('manager_id')     client_manager_id='manager_id'
    prop = get_object_or_404(PropertyManagement, pk=pk,)

    if request.method == 'POST':
        prop.delete()
        return redirect('clientmanager:property_list')

    return render(request, 'clientmanager/property/delete.html', {'property': prop})

# Building Services  ---------------------------------------------------------------------------------------------------------------
from mainapp.models import Vendor

# List vendors
def vendor_list(request):
    if not request.session.get('manager_id'):
        return redirect('clientmanager:client_login')
    vendors = Vendor.objects.all()
    return render(request, 'clientmanager/vendor/list.html', {'vendors': vendors})


def create_vendor(request):
    if not request.session.get('manager_id'):
        return redirect('clientmanager:client_login')

    if request.method == 'POST':
        # 1. Get selected checkbox services
        services = request.POST.getlist('service[]')  # list of checked values

        # 2. Get comma-separated custom services
        additional_services = request.POST.get('additional_service', '').strip()
        if additional_services:
            custom_list = [s.strip() for s in additional_services.split(',') if s.strip()]
            services.extend(custom_list)  # combine both

        # 3. Join all services into one string
        service_str = ','.join(services)

        Vendor.objects.create(
            company_name=request.POST.get('company_name'),
            username=request.POST.get('username'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone_number'),
            service=service_str,
        )
        return redirect('clientmanager:vendor_list')

    return render(request, 'clientmanager/vendor/create.html', {
        'service_choices': Vendor.SERVICE_CHOICES
    })


# Edit vendor
def edit_vendor(request, vendor_id):
    if not request.session.get('manager_id'):
        return redirect('clientmanager:client_login')

    vendor = get_object_or_404(Vendor, id=vendor_id)

    if request.method == 'POST':
        vendor.company_name = request.POST.get('company_name')
        vendor.username = request.POST.get('username')
        vendor.address = request.POST.get('address')
        vendor.city = request.POST.get('city')
        vendor.state = request.POST.get('state')
        vendor.zip_code = request.POST.get('zip_code')
        vendor.email = request.POST.get('email')
        vendor.phone_number = request.POST.get('phone_number')
        vendor.service = request.POST.get('service')
        vendor.save()
        return redirect('clientmanager:vendor_list')

    return render(request, 'clientmanager/vendor/edit.html', {'vendor': vendor})


# Delete vendor
def delete_vendor(request, vendor_id):
    if not request.session.get('manager_id'):
        return redirect('clientmanager:client_login')

    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.delete()
    return redirect('clientmanager:vendor_list')


# Client Manager Profile Update ---------------------------------------------------------------------------------------------------------------   
from django.shortcuts import render, redirect, get_object_or_404
from mainapp.models import ClientManagers

def clientmanager_profile_view(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')

    clientmanager = get_object_or_404(ClientManagers, id=manager_id)
    return render(request, 'clientmanager/profile/clientmanager_profile_view.html', {
        'clientmanager': clientmanager
    })


def clientmanager_profile_edit(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')

    clientmanager = get_object_or_404(ClientManagers, id=manager_id)

    if request.method == 'POST':
        clientmanager.first_name = request.POST.get('first_name')
        clientmanager.last_name = request.POST.get('last_name')
        clientmanager.email = request.POST.get('email')
        clientmanager.phone_number = request.POST.get('phone_number')
        clientmanager.city = request.POST.get('city')
        clientmanager.state = request.POST.get('state')
        clientmanager.zipcode = request.POST.get('zipcode')
        clientmanager.preferred_contact_method = request.POST.get('preferred_contact_method')

        if request.POST.get('password'):
            clientmanager.set_password(request.POST.get('password'))

        clientmanager.save()
        return redirect('clientmanager:clientmanager_profile_view')

    return render(request, 'clientmanager/profile/clientmanager_profile_edit.html', {
        'clientmanager': clientmanager,
        'contact_choices': ClientManagers.PREFERRED_CONTACT_CHOICES
    })


# Pre Arrival reqeust to client Manager ---------------------------------------------------------------------------------------------------------------
from servicedetails.models import PrearrivalInformation, Client

# View all requests

def clientmanager_prearrival_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')

    all_requests = PrearrivalInformation.objects.all().order_by('-id')

    return render(request, 'clientmanager/prearrival/prearrival_list.html', {
        'requests': all_requests
    })

# View single request
def clientmanager_prearrival_detail(request, request_id):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')

    request_detail = get_object_or_404(PrearrivalInformation, id=request_id)

    return render(request, 'clientmanager/prearrival/prearrival_detail.html', {
        'request_detail': request_detail
    })


# Departure requests ---------------------------------------------------------------------------------------------------------------
# views.py

from servicedetails.models import DepartureInformation

def clientmanager_departure_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')

    all_departure_requests = DepartureInformation.objects.all().order_by('-id')

    return render(request, 'clientmanager/departure/departure_list.html', {
        'requests': all_departure_requests
    })


def clientmanager_departure_detail(request, request_id):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')

    departure_request = get_object_or_404(DepartureInformation, id=request_id)

    return render(request, 'clientmanager/departure/departure_detail.html', {
        'request_detail': departure_request
    })


# Building pending completed denied services --------------------------------------------------------------------------------
# from django.shortcuts import render
# from django.shortcuts import render, redirect

# def client_manager_dashboard(request):
#     client_id = request.session.get('client_id')

#     if not client_id:
#         return redirect('clientmanager:client_login')  # or wherever your login page is

#     client_manager = ClientManagers.objects.get(id=client_id)
#     clients = Client.objects.filter(properties__client_manager=client_manager).distinct()

#     return render(request, 'client_manager_dashboard.html', {
#         'client_count': clients.count(),
#         'clients': clients,
#     })


# Building pending completed denied services --------------------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from servicedetails.models import ServiceRequest
from mainapp.models import Vendor

def pending_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')
    requests = ServiceRequest.objects.filter(status='pending')
    return render(request, 'clientmanager/servicerequests/pending.html', {'requests': requests})

def open_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')
    requests = ServiceRequest.objects.filter(status='open')
    return render(request, 'clientmanager/servicerequests/open.html', {'requests': requests})

def completed_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')
    requests = ServiceRequest.objects.filter(status='completed')
    return render(request, 'clientmanager/servicerequests/completed.html', {'requests': requests})

def denied_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')
    requests = ServiceRequest.objects.filter(status='denied')
    return render(request, 'clientmanager/servicerequests/denied.html', {'requests': requests})

def update_service_request(request, request_id):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')

    request_obj = get_object_or_404(ServiceRequest, id=request_id)
    vendors = Vendor.objects.all()

    if request.method == 'POST':
        request_obj.status = request.POST.get('status')
        vendor_id = request.POST.get('vendor')
        if vendor_id:
            request_obj.vendor = Vendor.objects.get(id=vendor_id)
        else:
            request_obj.vendor = None
        request_obj.save()
        messages.success(request, 'Request Updated Successfully!')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'clientmanager/servicerequests/update.html', {
        'request_obj': request_obj,
        'vendors': vendors,
    })

def service_request_detail(request, request_id):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')

    request_obj = get_object_or_404(ServiceRequest, id=request_id)

    return render(request, 'clientmanager/servicerequests/detail_view.html', {
        'request_obj': request_obj
    })

# Congiure Request ----------------------------------------------------------------------------------------------------------------------
from servicedetails.models import ConciergeServiceRequest

# Pending
def concierge_pending_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')
    requests = ConciergeServiceRequest.objects.filter(status='pending')
    return render(request, 'clientmanager/conciergerequests/pending.html', {'requests': requests})

# Open
def concierge_open_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')
    requests = ConciergeServiceRequest.objects.filter(status='open')
    return render(request, 'clientmanager/conciergerequests/open.html', {'requests': requests})

# Completed
def concierge_completed_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')
    requests = ConciergeServiceRequest.objects.filter(status='completed')
    return render(request, 'clientmanager/conciergerequests/completed.html', {'requests': requests})

# Denied
def concierge_denied_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')
    requests = ConciergeServiceRequest.objects.filter(status='denied')
    return render(request, 'clientmanager/conciergerequests/denied.html', {'requests': requests})

# Update
def update_concierge_request(request, request_id):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')

    request_obj = get_object_or_404(ConciergeServiceRequest, id=request_id)
    vendors = Vendor.objects.all()

    if request.method == 'POST':
        request_obj.status = request.POST.get('status')
        vendor_id = request.POST.get('vendor')
        if vendor_id:
            request_obj.vendor = Vendor.objects.get(id=vendor_id)
        else:
            request_obj.vendor = None
        request_obj.save()
        messages.success(request, 'Request Updated Successfully!')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'clientmanager/conciergerequests/update.html', {
        'request_obj': request_obj,
        'vendors': vendors,
    })

# View
def view_concierge_request(request, request_id):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')

    request_obj = get_object_or_404(ConciergeServiceRequest, id=request_id)
    return render(request, 'clientmanager/conciergerequests/view.html', {
        'request_obj': request_obj
    })


# property Improvement Request ---------------------------------------------------------------------------------------------------------------
from propertydetails.models import PropertyImprovement

# Pending
def property_pending_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')
    requests = PropertyImprovement.objects.filter(status='pending')
    return render(request, 'clientmanager/propertyimprovement/pending.html', {'requests': requests})

# Open
def property_open_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')
    requests = PropertyImprovement.objects.filter(status='open')
    return render(request, 'clientmanager/propertyimprovement/open.html', {'requests': requests})

# Completed
def property_completed_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')
    requests = PropertyImprovement.objects.filter(status='completed')
    return render(request, 'clientmanager/propertyimprovement/completed.html', {'requests': requests})

# Denied
def property_denied_requests(request):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')
    requests = PropertyImprovement.objects.filter(status='denied')
    return render(request, 'clientmanager/propertyimprovement/denied.html', {'requests': requests})

# Update
def update_property_request(request, request_id):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')

    request_obj = get_object_or_404(PropertyImprovement, id=request_id)
    vendors = Vendor.objects.all()

    if request.method == 'POST':
        status = request.POST.get('status')
        cost = request.POST.get('cost')
        vendor_id = request.POST.get('vendor')

        if status:
            request_obj.status = status

        if cost:
            request_obj.cost = cost

        if vendor_id:
            try:
                request_obj.vendor = Vendor.objects.get(id=vendor_id)
            except Vendor.DoesNotExist:
                request_obj.vendor = None

        request_obj.save()
        messages.success(request, 'Request Updated Successfully!')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'clientmanager/propertyimprovement/update.html', {
        'request_obj': request_obj,
        'vendors': vendors,
    })

# View
def view_property_request(request, request_id):
    manager_id = request.session.get('manager_id') 
    if not manager_id:
        return redirect('clientmanager:client_login')

    request_obj = get_object_or_404(PropertyImprovement, id=request_id)
    return render(request, 'clientmanager/propertyimprovement/view.html', {
        'request_obj': request_obj
    })


# Building WALKTHROUGH REPORT ------------------------------------------------------------------------------------------
from django.shortcuts import render
from django.http import HttpResponse
from walkthroughreport.models import WalkthroughReport
from mainapp.models import Client
from django.views.decorators.csrf import csrf_exempt

# def submit_walkthrough(request):
#     if request.method == "POST":
#         data = request.POST

#         # Only set fields that are present
#         kwargs = {}
#         if data.get("user"):
#             try:
#                 kwargs["user"] = Client.objects.get(id=data.get("user"))
#             except Client.DoesNotExist:
#                 return HttpResponse("Invalid client", status=400)

#         for field in WalkthroughReport._meta.get_fields():
#             if field.name in data and field.name != 'user':
#                 val = data.get(field.name)
#                 if val != "":
#                     kwargs[field.name] = val

#         WalkthroughReport.objects.create(**kwargs)
#         return HttpResponse("Submitted Successfully")
    
#     clients = Client.objects.all()
#     return render(request, "clientmanager/walkthrough/submit_walkthrough.html", {"clients": clients})

from django import forms

class WalkthroughReportForm(forms.ModelForm):
    class Meta:
        model = WalkthroughReport
        fields = '__all__'

def walkthrough_report_view(request):
    if request.method == 'POST':
        form = WalkthroughReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientmanager:walkthrough-success')
    else:
        form = WalkthroughReportForm()
    return render(request, 'walkthrough_form.html', {'form': form})

def walkthrough_success_view(request):
    return render(request, 'walkthrough_success.html')



# Client Management 
from django.shortcuts import render, get_object_or_404, redirect
from mainapp.models import Client

def client_list_page(request):
    clients = Client.objects.all()
    return render(request, 'clientmanager/client/client_list_page.html', {'clients': clients})

def client_edit_page(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        client.first_name = request.POST.get('first_name')
        client.last_name = request.POST.get('last_name')
        client.username = request.POST.get('username')
        client.email = request.POST.get('email')
        client.address = request.POST.get('address')
        client.city = request.POST.get('city')
        client.state = request.POST.get('state')
        client.zipcode = request.POST.get('zipcode')
        client.phone_number = request.POST.get('phone_number')
        client.preferred_contact_method = request.POST.get('preferred_contact_method')
        
        client.contact1_name = request.POST.get('contact1_name')
        client.contact1_email = request.POST.get('contact1_email')
        client.contact1_phone = request.POST.get('contact1_phone')
        client.contact1_preferred = request.POST.get('contact1_preferred')

        client.contact2_name = request.POST.get('contact2_name')
        client.contact2_email = request.POST.get('contact2_email')
        client.contact2_phone = request.POST.get('contact2_phone')
        client.contact2_preferred = request.POST.get('contact2_preferred')

        client.contact3_name = request.POST.get('contact3_name')
        client.contact3_email = request.POST.get('contact3_email')
        client.contact3_phone = request.POST.get('contact3_phone')
        client.contact3_preferred = request.POST.get('contact3_preferred')

        client.save()
        return redirect('clientmanager:client_list_page')

    return render(request, 'clientmanager/client/client_edit_page.html', {'client': client})


def create_new_client_view(request):
    if request.method == 'POST':
        Client.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zipcode=request.POST.get('zipcode'),
            phone_number=request.POST.get('phone_number'),
            preferred_contact_method=request.POST.get('preferred_contact_method'),
            contact1_name=request.POST.get('contact1_name'),
            contact1_email=request.POST.get('contact1_email'),
            contact1_phone=request.POST.get('contact1_phone'),
            contact1_preferred=request.POST.get('contact1_preferred'),
            contact2_name=request.POST.get('contact2_name'),
            contact2_email=request.POST.get('contact2_email'),
            contact2_phone=request.POST.get('contact2_phone'),
            contact2_preferred=request.POST.get('contact2_preferred'),
            contact3_name=request.POST.get('contact3_name'),
            contact3_email=request.POST.get('contact3_email'),
            contact3_phone=request.POST.get('contact3_phone'),
            contact3_preferred=request.POST.get('contact3_preferred'),
        )
        return redirect('client_list_view')  # change if needed
    return render(request, 'clientmanager/client/create.html')