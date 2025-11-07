from django.shortcuts import render
from django.shortcuts import render, redirect
from mainapp.models import ClientManagers
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

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

def admin_dashboard(request):
    return render(request, 'clientmanager/dashboard.html')

# Building Property  ---------------------------------------------------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from propertydetails.models import PropertyManagement
from django.contrib import messages
from mainapp.models import Client, ClientManagers  # or whatever your models are named
from propertydetails.models import PropertyManagement, Floor, Room
from django.db import transaction
from django.core.exceptions import ValidationError
# def get_client_manager_id(request):
#     return request.session.get('client_id')


from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
import json
# decorators.py
from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden


from .decorators import client_manager_required

@client_manager_required
def property_list_view(request):
    logged_in_cm = request.client_manager
    
    if request.method == "POST":
        property_id = request.POST.get("property_id")
        cm_id = request.POST.get("cm_id")

        prop = get_object_or_404(PropertyManagement, id=property_id, client_manager=logged_in_cm)
        cm = get_object_or_404(ClientManagers, id=cm_id)
        prop.client_manager = cm
        prop.save()
        return redirect('clientmanager:property_list')

    clients = Client.objects.all()
    properties = PropertyManagement.objects.filter(client_manager=logged_in_cm)
    all_cms = ClientManagers.objects.all()

    all_cms_json = json.dumps([
        {
            "id": cm.id,
            "name": f"{cm.last_name}, {cm.first_name}",
            "email": cm.email,
            "phone": cm.phone_number or cm.office_phone or ""
        } for cm in all_cms
    ], cls=DjangoJSONEncoder)

    return render(request, 'clientmanager/property/list.html', {
        'properties': properties,
        'clients': clients,
        'all_cms_json': all_cms_json
    })


def property_detail_view(request, pk):
    prop = get_object_or_404(
        PropertyManagement.objects.prefetch_related('floors__rooms'), pk=pk
    )
    return render(request, 'clientmanager/property/detail.html', {'property': prop})

US_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

def property_create_view(request):
    clients = Client.objects.all()
    managers = ClientManagers.objects.all()
    context = {
        'clients': clients,
        'managers': managers,
        'us_states': US_STATES,
    }

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Get client_id if selected
                property_pic = request.FILES.get('property_pic')
                client_id = request.POST.get('client_id')
                
                # If no existing client selected, try creating a new one
                if not client_id:
                    new_first_name = request.POST.get('new_first_name', '')
                    new_last_name = request.POST.get('new_last_name', '')
                    new_email = request.POST.get('new_email', '')
                    new_username = ''
                    new_password = ''
                    new_phone = request.POST.get('new_phone', '')
                    office_phone = request.POST.get('office_phone', '')  
                    business_address = request.POST.get('business_address', '')
                    address = request.POST.get('client_address', '')
                    city = request.POST.get('client_city', '')
                    state = request.POST.get('client_state', '')
                    zipcode = request.POST.get('client_zipcode', '')
                    
                    contact1_name = request.POST.get('contact1_name', '')
                    contact1_last_name = request.POST.get('contact1_last_name', '')
                    contact1_email = request.POST.get('contact1_email', '')
                    contact1_phone = request.POST.get('contact1_phone', '')
                    contact1_office_phone = request.POST.get('contact1_office_phone', '')
                    contact1_buisness_adress = request.POST.get('contact1_buisness_adress', '')
                    contact1_priority = request.POST.get('contact1_priority', '')

                    # Contact 2 (Secondary)
                    contact2_name = request.POST.get('contact2_name', '')
                    contact2_last_name = request.POST.get('contact2_last_name', '')
                    contact2_email = request.POST.get('contact2_email', '')
                    contact2_phone = request.POST.get('contact2_phone', '')
                    contact2_office_phone = request.POST.get('contact2_office_phone', '')
                    contact2_buisness_adress = request.POST.get('contact2_buisness_adress', '')
                    contact2_priority = request.POST.get('contact2_priority', '')

                    # Contact 3 (Tertiary)
                    contact3_name = request.POST.get('contact3_name', '')
                    contact3_last_name = request.POST.get('contact3_last_name', '')
                    contact3_email = request.POST.get('contact3_email', '')
                    contact3_phone = request.POST.get('contact3_phone', '')
                    contact3_office_phone = request.POST.get('contact3_office_phone', '')
                    contact3_buisness_adress = request.POST.get('contact3_buisness_adress', '')
                    contact3_priority = request.POST.get('contact3_priority', '')

                    # Contact 4
                    contact4_name = request.POST.get('contact4_name', '')
                    contact4_last_name = request.POST.get('contact4_last_name', '')
                    contact4_email = request.POST.get('contact4_email', '')
                    contact4_phone = request.POST.get('contact4_phone', '')
                    contact4_office_phone = request.POST.get('contact4_office_phone', '')
                    contact4_buisness_adress = request.POST.get('contact4_buisness_adress', '')
                    contact4_priority = request.POST.get('contact4_priority', '')

                    # Contact 5
                    contact5_name = request.POST.get('contact5_name', '')
                    contact5_last_name = request.POST.get('contact5_last_name', '')
                    contact5_email = request.POST.get('contact5_email', '')
                    contact5_phone = request.POST.get('contact5_phone', '')
                    contact5_office_phone = request.POST.get('contact5_office_phone', '')
                    contact5_buisness_adress = request.POST.get('contact5_buisness_adress', '')
                    contact5_priority = request.POST.get('contact5_priority', '')

                    # Only require basic client information if creating a new client
                    if new_first_name or new_last_name or new_username or new_email:
                        if not all([new_first_name, new_last_name, new_email]):
                            error_message = "Please complete all required fields for the new client"
                            context['error_message'] = error_message
                            return render(request, 'clientmanager/property/create.html', context)

                        # Create new client
                        new_client = Client.objects.create(
                            first_name=new_first_name,
                            last_name=new_last_name,
                            email=new_email,
                            phone_number=new_phone,
                            office_phone=office_phone,
                            business_address=business_address,
                            address=address,
                            city=city,
                            state=state,
                            zipcode=zipcode,
                            
                            contact1_name=contact1_name,
                            contact1_last_name=contact1_last_name,
                            contact1_email=contact1_email,
                            contact1_phone=contact1_phone,
                            contact1_office_phone=contact1_office_phone,
                            contact1_buisness_adress=contact1_buisness_adress,
                            contact1_priority=contact1_priority,

                            contact2_name=contact2_name,
                            contact2_last_name=contact2_last_name,
                            contact2_email=contact2_email,
                            contact2_phone=contact2_phone,
                            contact2_office_phone=contact2_office_phone,
                            contact2_buisness_adress=contact2_buisness_adress,
                            contact2_priority=contact2_priority,

                            contact3_name=contact3_name,
                            contact3_last_name=contact3_last_name,
                            contact3_email=contact3_email,
                            contact3_phone=contact3_phone,
                            contact3_office_phone=contact3_office_phone,
                            contact3_buisness_adress=contact3_buisness_adress,
                            contact3_priority=contact3_priority,

                            contact4_name=contact4_name,
                            contact4_last_name=contact4_last_name,
                            contact4_email=contact4_email,
                            contact4_phone=contact4_phone,
                            contact4_office_phone=contact4_office_phone,
                            contact4_buisness_adress=contact4_buisness_adress,
                            contact4_priority=contact4_priority,

                            contact5_name=contact5_name,
                            contact5_last_name=contact5_last_name,
                            contact5_email=contact5_email,
                            contact5_phone=contact5_phone,
                            contact5_office_phone=contact5_office_phone,
                            contact5_buisness_adress=contact5_buisness_adress,
                            contact5_priority=contact5_priority,
                        )
                        client_id = new_client.id
                
                # Handle client manager - either get existing or create new
                client_manager_id = request.POST.get('client_manager_id')
                
                # Check if new client manager info was provided
                new_cm_first_name = request.POST.get('new_cm_first_name', '')
                new_cm_last_name = request.POST.get('new_cm_last_name', '')
                new_cm_username = request.POST.get('new_cm_username', '')
                new_cm_email = request.POST.get('new_cm_email', '')
                new_cm_password = request.POST.get('new_cm_password', '')
                new_cm_phone = request.POST.get('new_cm_phone', '')
                office_cm_phone = request.POST.get('office_cm_phone', '')
                buisness_cm_adress = request.POST.get('buisness_cm_adress', '')
                
                # If new client manager details were provided, create a new client manager
                if new_cm_first_name or new_cm_last_name or new_cm_username or new_cm_email:
                    if not all([new_cm_first_name, new_cm_last_name, new_cm_username, new_cm_email, new_cm_password]):
                        error_message = "Please complete all required fields for the new client manager"
                        context['error_message'] = error_message
                        return render(request, 'clientmanager/property/create.html', context)
                    
                    # Create new client manager
                    new_manager = ClientManagers.objects.create(
                        first_name=new_cm_first_name,
                        last_name=new_cm_last_name,
                        username=new_cm_username,
                        email=new_cm_email,
                        password=new_cm_password,
                        phone_number=new_cm_phone,
                        office_phone=office_cm_phone,
                        business_address=buisness_cm_adress,
                    )
                    client_manager_id = new_manager.id
                
                # Validate property fields
                address = request.POST.get('address')
                if not address:
                    error_message = "Property address is required"
                    context['error_message'] = error_message
                    return render(request, 'clientmanager/property/create.html', context)
                
                if not client_id:
                    error_message = "Please select or create a client"
                    context['error_message'] = error_message
                    return render(request, 'clientmanager/property/create.html', context)
                    
                if not client_manager_id:
                    error_message = "Please select or create a client manager"
                    context['error_message'] = error_message
                    return render(request, 'clientmanager/property/create.html', context)

                # Create the Property
                prop = PropertyManagement.objects.create(
                    client_id=client_id,
                    client_manager_id=client_manager_id,
                    address=address,
                    street_line1 = request.POST.get('street_line1', ''),
                    street_line2 = request.POST.get('street_line2', ''),
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
                    state=request.POST.get('state', ''),
                    city=request.POST.get('city', ''),
                    zipcode=request.POST.get('property_zipcode', ''),
                    additional_info=request.POST.get('additional_info', ''),

                    # New features
                    basketball_court='basketball_court' in request.POST,
                    tennis_court='tennis_court' in request.POST,
                    pickleball_court='pickleball_court' in request.POST,
                    hot_tub='hot_tub' in request.POST,
                    outdoor_kitchen_gazebo='outdoor_kitchen_gazebo' in request.POST,
                    waterfront='waterfront' in request.POST,

                    property_pic=property_pic,
                )

                # Loop through each floor and room
                floor_count = len([k for k in request.POST if k.startswith('floor_name_')])
                for i in range(1, floor_count + 1):
                    floor_name = request.POST.get(f'floor_name_{i}')
                    if not floor_name:
                        continue
                    
                    # Handle floor image
                    floor_image = request.FILES.get(f'floor_image_{i}')

                    # Create floor with image handling
                    floor = Floor.objects.create(
                        property=prop,
                        floor_name=floor_name,
                        floor_imgae=floor_image,  # Keeping original field name
                    )

                    # Now handle rooms under this floor
                    room_count = len([k for k in request.POST if k.startswith(f'room_name_{i}_')])

                    for j in range(1, room_count + 1):
                        room_name = request.POST.get(f'room_name_{i}_{j}')
                        room_size = request.POST.get(f'room_size_{i}_{j}')

                        if room_name:
                            Room.objects.create(
                                floor=floor,
                                room_name=room_name,
                            )

                return redirect('clientmanager:property_list')

        except Exception as e:
            import traceback
            print("Error occurred:", str(e))
            print(traceback.format_exc())  # More detailed error for debugging
            context['error_message'] = f"Error: {str(e)}"
            return render(request, 'clientmanager/property/create.html', context)

    return render(request, 'clientmanager/property/create.html', context)



from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password
def property_update_view(request, pk):
    prop = get_object_or_404(PropertyManagement, pk=pk)
    client = prop.client
    client_managers = ClientManagers.objects.all()
    if 'delete_property_pic' in request.POST:
        prop.property_pic.delete(save=True)
    if request.method == 'POST':
        # Handling Property and Client Info Updates
        if 'address' in request.POST:
            # Property fields
            prop.address = request.POST['address']
            prop.street_line1 = request.POST.get('street1', '')
            prop.street_line2 = request.POST.get('street2', '')
            prop.size_of_home = request.POST.get('size_of_home', '')
            prop.number_of_stories = request.POST.get('number_of_stories', '')
            prop.construction_type = request.POST.get('construction_type', '')
            prop.year_built = request.POST.get('year_built', '')
            prop.has_pool = 'has_pool' in request.POST
            prop.gated_community = 'gated_community' in request.POST
            prop.impact_windows = 'impact_windows' in request.POST
            prop.has_hoa = 'has_hoa' in request.POST
            prop.gated_property = 'gated_property' in request.POST
            prop.basketball_court = 'basketball_court' in request.POST
            prop.tennis_court = 'tennis_court' in request.POST
            prop.pickleball_court = 'pickleball_court' in request.POST
            prop.hot_tub = 'hot_tub' in request.POST
            prop.outdoor_kitchen_gazebo = 'outdoor_kitchen_gazebo' in request.POST
            prop.waterfront = 'waterfront' in request.POST

            prop.state = request.POST.get('property_state', '')   # Added state
            prop.city = request.POST.get('property_city', '')     # Added City 
            prop.preferred_contact_method = request.POST.get('preferred_contact_method', 'email')
            prop.zipcode = request.POST.get('property_zipcode', '')     # Added City 
            prop.additional_info = request.POST.get('additional_info', '')
            property_pic = request.FILES.get('property_pic')
            if property_pic:
                prop.property_pic = property_pic
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
            new_password = request.POST.get('client_password', '')
            if new_password and not new_password.startswith('pbkdf2_'):
                client.password = make_password(new_password)

            # Update contact persons info (if necessary)
            # Contact Person 1
            client.contact1_name = request.POST.get('contact1_name', '')
            client.contact1_last_name = request.POST.get('contact1_last_name', '')
            client.contact1_email = request.POST.get('contact1_email', '')
            client.contact1_phone = request.POST.get('contact1_phone', '')
            client.contact1_office_phone = request.POST.get('contact1_office_phone', '')
            client.contact1_buisness_adress = request.POST.get('contact1_buisness_adress', '')
            client.contact1_preferred = request.POST.get('contact1_preferred', '')
            client.contact1_priority = request.POST.get('contact1_priority', '')

            # Contact Person 2 Update
            client.contact2_name = request.POST.get('contact2_name', '')
            client.contact2_last_name = request.POST.get('contact2_last_name', '')
            client.contact2_email = request.POST.get('contact2_email', '')
            client.contact2_phone = request.POST.get('contact2_phone', '')
            client.contact2_office_phone = request.POST.get('contact2_office_phone', '')
            client.contact2_buisness_adress = request.POST.get('contact2_buisness_adress', '')
            client.contact2_preferred = request.POST.get('contact2_preferred', '')
            client.contact2_priority = request.POST.get('contact2_priority', '')

            # Contact Person 3 Update
            client.contact3_name = request.POST.get('contact3_name', '')
            client.contact3_last_name = request.POST.get('contact3_last_name', '')
            client.contact3_email = request.POST.get('contact3_email', '')
            client.contact3_phone = request.POST.get('contact3_phone', '')
            client.contact3_office_phone = request.POST.get('contact3_office_phone', '')
            client.contact3_buisness_adress = request.POST.get('contact3_buisness_adress', '')
            client.contact3_preferred = request.POST.get('contact3_preferred', '')
            client.contact3_priority = request.POST.get('contact3_priority', '')

            # Contact Person 4 Update
            client.contact4_name = request.POST.get('contact4_name', '')
            client.contact4_last_name = request.POST.get('contact4_last_name', '')
            client.contact4_email = request.POST.get('contact4_email', '')
            client.contact4_phone = request.POST.get('contact4_phone', '')
            client.contact4_office_phone = request.POST.get('contact4_office_phone', '')
            client.contact4_buisness_adress = request.POST.get('contact4_buisness_adress', '')
            client.contact4_preferred = request.POST.get('contact4_preferred', '')
            client.contact4_priority = request.POST.get('contact4_priority', '')

            # Contact Person 4 Update
            client.contact5_name = request.POST.get('contact4_name', '')
            client.contact5_last_name = request.POST.get('contact4_last_name', '')
            client.contact5_email = request.POST.get('contact4_email', '')
            client.contact5_phone = request.POST.get('contact4_phone', '')
            client.contact5_office_phone = request.POST.get('contact4_office_phone', '')
            client.contact5_buisness_adress = request.POST.get('contact4_buisness_adress', '')
            client.contact5_preferred = request.POST.get('contact4_preferred', '')
            client.contact5_priority = request.POST.get('contact4_priority', '')

            client.save()

            # Update floors and rooms (including floor image)
            # Replace the floor and room handling section in your property_update_view with this:

            # Update floors and rooms (including floor image)
            existing_floors = list(prop.floors.all())
            floors_to_keep = []

            # Get all floor names from POST data
            floor_names_in_post = []
            i = 1
            while True:
                floor_key = f'floor_name_{i}'
                if floor_key not in request.POST:
                    break
                floor_names_in_post.append((i, request.POST.get(floor_key)))
                i += 1

            # Process each floor from POST data
            for floor_index, floor_name in floor_names_in_post:
                floor_image = request.FILES.get(f'floor_image_{floor_index}')
                
                # Try to find existing floor by index (if it exists)
                floor = None
                if floor_index <= len(existing_floors):
                    floor = existing_floors[floor_index - 1]
                    floor.floor_name = floor_name
                    if floor_image:
                        floor.floor_imgae = floor_image
                    floor.save()
                else:
                    # Create new floor
                    floor = Floor.objects.create(
                        property=prop, 
                        floor_name=floor_name, 
                        floor_imgae=floor_image
                    )
                
                floors_to_keep.append(floor)
                
                # Handle room updates for this floor
                existing_rooms = list(floor.rooms.all())
                rooms_to_keep = []
                
                j = 1
                while True:
                    room_name_key = f'room_name_{floor_index}_{j}'
                    room_size_key = f'room_size_{floor_index}_{j}'
                    
                    if room_name_key not in request.POST:
                        break
                    
                    room_name = request.POST.get(room_name_key)
                    room_size = request.POST.get(room_size_key, '')
                    
                    if j <= len(existing_rooms):
                        # Update existing room
                        room = existing_rooms[j - 1]
                        room.room_name = room_name
                        room.room_size = room_size
                        room.save()
                    else:
                        # Create new room
                        room = Room.objects.create(
                            floor=floor,
                            room_name=room_name,
                            room_size=room_size
                        )
                    
                    rooms_to_keep.append(room)
                    j += 1
                
                # Delete rooms that are no longer in the form
                for room in existing_rooms:
                    if room not in rooms_to_keep:
                        room.delete()

            # Delete floors that are no longer in the form
            for floor in existing_floors:
                if floor not in floors_to_keep:
                    floor.delete()

        # Handling Client Manager Update (if new_cm is present)
        if 'new_cm' in request.POST:
            client_manager_id = request.POST.get('new_cm')
            if client_manager_id:
                client_manager = get_object_or_404(ClientManagers, pk=client_manager_id)
                prop.client_manager = client_manager
                prop.save()

        return redirect('clientmanager:property_list')

    floors = prop.floors.prefetch_related('rooms').all()
    return render(request, 'clientmanager/property/edit.html', {
        'property': prop,
        'floors': floors,
        'client': client,
        'client_managers': client_managers,
        'selected_client_manager': prop.client_manager,
        'us_states': US_STATES,  # ✅ Pass it to the template
    })


# def property_update_view(request, pk):
#     prop = get_object_or_404(PropertyManagement, pk=pk)
#     client_managers = ClientManagers.objects.all()

#     if request.method == 'POST':
#         submitted_cm_id = request.POST.get('new_cm')
#         print("Submitted CM ID:", submitted_cm_id)

#         if submitted_cm_id:
#             new_cm = get_object_or_404(ClientManagers, pk=submitted_cm_id)
#             prop.client_manager = new_cm
#             prop.save()
#             print("Client Manager updated to:", new_cm.id)

#         return redirect('clientmanager:property_list')

#     return render(request, 'clientmanager/property/edit.html', {
#         'property': prop,
#         'client_managers': client_managers
#     })



from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.conf import settings
import os
from django.shortcuts import get_object_or_404

from mainapp.models import Vendor
import uuid
from mainapp.models import Vendor, VendorContact

def property_delete_view(request, pk):
    prop = get_object_or_404(PropertyManagement, pk=pk)

    if request.method == 'POST':
        prop.delete()
        return redirect('clientmanager:property_list')

    return render(request, 'clientmanager/property/delete.html', {'property': prop})

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

# Starting of vendor -----------------------------------------------------------------------------------------------------------------
US_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]
from mainapp.models import Vendor, VendorServices
# List vendors
from mainapp.models import Vendor, VendorContact

def vendor_list(request):
    vendors = Vendor.objects.prefetch_related('contacts').all()
    
    # Add first service to each vendor
    for vendor in vendors:
        if vendor.service:
            vendor.first_service = vendor.service.split(',')[0].strip()
        else:
            vendor.first_service = ''
    
    return render(request, 'clientmanager/vendor/list.html', {'vendors': vendors})


def create_vendor(request):
    if request.method == 'POST':
        # Handle new service creation
        new_service = request.POST.get('new_service', '').strip()
        if new_service:
            # Check if service already exists
            if not VendorServices.objects.filter(service__iexact=new_service).exists():
                VendorServices.objects.create(service=new_service)
        
        # Get main service and additional services
        main_service = request.POST.get('main_service', '')
        additional_service_1 = request.POST.get('additional_service_1', '')
        additional_service_2 = request.POST.get('additional_service_2', '')
        
        # Combine all services
        combined_services = []
        if main_service:
            combined_services.append(main_service)
        if additional_service_1:
            combined_services.append(additional_service_1)
        if additional_service_2:
            combined_services.append(additional_service_2)

        # Create new vendor
        vendor = Vendor.objects.create(
            company_name=request.POST.get('company_name'),
            street=request.POST.get('street'),
            website=request.POST.get('website'),
            suite=request.POST.get('suite'),
            notes=request.POST.get('notes'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            phone_number=request.POST.get('phone_number'),
            service=', '.join(combined_services),
        )

        # Create contacts
        contact_first_names = request.POST.getlist('contact_first_name[]')
        contact_last_names = request.POST.getlist('contact_last_name[]')
        contact_cells = request.POST.getlist('contact_cell[]')
        contact_emails = request.POST.getlist('contact_email[]')

        for i in range(len(contact_first_names)):
            if contact_first_names[i].strip() and contact_last_names[i].strip():
                VendorContact.objects.create(
                    vendor=vendor,
                    first_name=contact_first_names[i].strip(),
                    last_name=contact_last_names[i].strip(),
                    cell=contact_cells[i].strip() if i < len(contact_cells) else '',
                    email=contact_emails[i].strip() if i < len(contact_emails) else ''
                )

        return redirect('clientmanager:vendor_list')

    # Get services from database
    vendor_services = VendorServices.objects.all().order_by('service')

    context = {
        'vendor_services': vendor_services,
        'US_STATES': US_STATES,
    }

    return render(request, 'clientmanager/vendor/create.html', context)

def edit_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)

    if request.method == 'POST':
        # Get main service and additional services
        main_service = request.POST.get('main_service', '')
        additional_service_1 = request.POST.get('additional_service_1', '')
        additional_service_2 = request.POST.get('additional_service_2', '')
        
        # Combine all services
        combined_services = []
        if main_service:
            combined_services.append(main_service)
        if additional_service_1:
            combined_services.append(additional_service_1)
        if additional_service_2:
            combined_services.append(additional_service_2)

        # Update vendor fields
        vendor.company_name = request.POST.get('company_name')
        vendor.street = request.POST.get('street')
        vendor.website = request.POST.get('website')
        vendor.suite = request.POST.get('suite')
        vendor.notes = request.POST.get('notes')
        vendor.city = request.POST.get('city')
        vendor.state = request.POST.get('state')
        vendor.zip_code = request.POST.get('zip_code')
        vendor.phone_number = request.POST.get('phone_number')
        vendor.service = ', '.join(combined_services)
        vendor.save()

        # Handle contacts - delete existing and create new ones
        VendorContact.objects.filter(vendor=vendor).delete()

        contact_first_names = request.POST.getlist('contact_first_name[]')
        contact_last_names = request.POST.getlist('contact_last_name[]')
        contact_cells = request.POST.getlist('contact_cell[]')
        contact_emails = request.POST.getlist('contact_email[]')

        for i in range(len(contact_first_names)):
            if contact_first_names[i].strip() and contact_last_names[i].strip():
                VendorContact.objects.create(
                    vendor=vendor,
                    first_name=contact_first_names[i].strip(),
                    last_name=contact_last_names[i].strip(),
                    cell=contact_cells[i].strip() if i < len(contact_cells) else '',
                    email=contact_emails[i].strip() if i < len(contact_emails) else ''
                )

        return redirect('clientmanager:vendor_list')

    # Get existing data
    existing_contacts = VendorContact.objects.filter(vendor=vendor)
    existing_services = [s.strip() for s in vendor.service.split(',')] if vendor.service else []
    
    # Parse existing services
    main_service = existing_services[0] if existing_services else ''
    additional_service_1 = existing_services[1] if len(existing_services) > 1 else ''
    additional_service_2 = existing_services[2] if len(existing_services) > 2 else ''

    # Get services from database
    vendor_services = VendorServices.objects.all().order_by('service')

    context = {
        'vendor': vendor,
        'existing_contacts': existing_contacts,
        'main_service': main_service,
        'additional_service_1': additional_service_1,
        'additional_service_2': additional_service_2,
        'vendor_services': vendor_services,
        'US_STATES': US_STATES,
    }

    return render(request, 'clientmanager/vendor/edit.html', context)
def vendor_details(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)

    # Get existing contacts
    existing_contacts = VendorContact.objects.filter(vendor=vendor)
    existing_services = [s.strip() for s in vendor.service.split(',')] if vendor.service else []

    # Parse services
    main_service = existing_services[0] if existing_services else ''
    additional_service_1 = existing_services[1] if len(existing_services) > 1 else ''
    additional_service_2 = existing_services[2] if len(existing_services) > 2 else ''

    # Get services from database (if you want to show full list for reference)
    vendor_services = VendorServices.objects.all().order_by('service')

    context = {
        'vendor': vendor,
        'existing_contacts': existing_contacts,
        'main_service': main_service,
        'additional_service_1': additional_service_1,
        'additional_service_2': additional_service_2,
        'vendor_services': vendor_services,
        'US_STATES': US_STATES,
    }

    return render(request, 'clientmanager/vendor/details.html', context)

# Delete vendor
def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.delete()
    return redirect('clientmanager:vendor_list')

def manage_vendor_services(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            service_name = request.POST.get('service', '').strip()
            if service_name:
                if VendorServices.objects.filter(service__iexact=service_name).exists():
                    messages.error(request, 'This service already exists.')
                else:
                    VendorServices.objects.create(service=service_name)
                    messages.success(request, 'Service added successfully.')
            else:
                messages.error(request, 'Service name is required.')
        
        elif action == 'edit':
            service_id = request.POST.get('service_id')
            service_name = request.POST.get('service', '').strip()
            if service_id and service_name:
                service = get_object_or_404(VendorServices, id=service_id)
                if VendorServices.objects.filter(service__iexact=service_name).exclude(id=service_id).exists():
                    messages.error(request, 'This service name already exists.')
                else:
                    service.service = service_name
                    service.save()
                    messages.success(request, 'Service updated successfully.')
            else:
                messages.error(request, 'Service name is required.')
        
        elif action == 'delete':
            service_id = request.POST.get('service_id')
            if service_id:
                service = get_object_or_404(VendorServices, id=service_id)
                service_name = service.service
                service.delete()
                messages.success(request, f'Service "{service_name}" deleted successfully.')
    
    services = VendorServices.objects.all().order_by('service')
    context = {
        'services': services
    }
    return render(request, 'clientmanager/vendor/manage.html', context)


# Building pending completed denied services ----------------------------------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from servicedetails.models import ServiceRequest
from mainapp.models import Vendor

def pending_requests(request):
    requests = ServiceRequest.objects.filter(status='pending')
    return render(request, 'clientmanager/servicerequests/pending.html', {'requests': requests})

from django.db.models import Q

def open_requests(request):
    # Show all except if both are approved and completed OR both are denied
    requests = ServiceRequest.objects.exclude(
        Q(status='completed', client_approval='Approved') |
        Q(status='denied', client_approval='Denied')
    )
    return render(request, 'clientmanager/servicerequests/open.html', {'requests': requests})

def completed_requests(request):
    # Only if both are completed and approved
    requests = ServiceRequest.objects.filter(status='completed', client_approval='Approved')
    return render(request, 'clientmanager/servicerequests/completed.html', {'requests': requests})

def denied_requests(request):
    # Only if both are denied
    requests = ServiceRequest.objects.filter(status='denied', client_approval='Denied')
    return render(request, 'clientmanager/servicerequests/denied.html', {'requests': requests})

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from django.contrib import messages

def update_service_request(request, request_id):
    request_obj = get_object_or_404(ServiceRequest, id=request_id)
    vendors = Vendor.objects.all()

    if request.method == 'POST':
        request_obj.status = request.POST.get('status')

        # Handle vendor
        vendor_id = request.POST.get('vendor')
        if vendor_id:
            request_obj.vendor = Vendor.objects.get(id=vendor_id)
        else:
            request_obj.vendor = None

        # Get and validate completation_denied_date
        date_str = request.POST.get('completation_denied_date')
        print("DEBUG - Received date:", date_str)  # For debugging in terminal

        parsed_date = parse_date(date_str)
        if not parsed_date:
            messages.error(request, "Completation Denied Date is required and must be valid.")
            return render(request, 'clientmanager/servicerequests/update.html', {
                'request_obj': request_obj,
                'vendors': vendors,
            })

        request_obj.completation_denied_date = parsed_date
        request_obj.save()

        return redirect('clientmanager:clientmanager_open_requests')

    return render(request, 'clientmanager/servicerequests/update.html', {
        'request_obj': request_obj,
        'vendors': vendors,
    })


def service_request_detail(request, request_id):
    request_obj = get_object_or_404(ServiceRequest, id=request_id)

    return render(request, 'clientmanager/servicerequests/detail_view.html', {
        'request_obj': request_obj
    })



# Service reqiuest new part starts here -------------------------------------------------------------------------
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def update_service_cost(request):
    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        amount = data.get('amount')
        remarks = data.get('remarks', '')
        
        service_request = get_object_or_404(ServiceRequest, id=request_id)
        service_request.cost = amount
        service_request.cost_remarks = remarks
        service_request.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
def modify_client_approval(request):
    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        approval_status = data.get('approval_status')
        
        service_request = get_object_or_404(ServiceRequest, id=request_id)
        service_request.client_approval = approval_status
        service_request.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
def change_request_status(request):
    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        status = data.get('status')
        completion_date = data.get('completion_date')
        remarks = data.get('remarks', '')
        
        service_request = get_object_or_404(ServiceRequest, id=request_id)
        service_request.status = status
        
        if completion_date:
            from datetime import datetime
            service_request.completation_denied_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
        
        service_request.status_remarks = remarks
        service_request.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    




# Consiguerge requests -------------------------------------------------------------------------------------------------
from servicedetails.models import ConciergeServiceRequest

# Pending
def concierge_pending_requests(request):
    requests = ConciergeServiceRequest.objects.filter(status='pending')
    return render(request, 'clientmanager/conciergerequests/pending.html', {'requests': requests})

from django.db.models import Q

# Open
def concierge_open_requests(request):
    # Show all except if both are approved and completed OR both are denied
    requests = ConciergeServiceRequest.objects.exclude(
        Q(status='completed', client_approval='Approved') |
        Q(status='denied', client_approval='Denied')
    )
    return render(request, 'clientmanager/conciergerequests/open.html', {'requests': requests})

# Completed
def concierge_completed_requests(request):
    # Only if both are completed and approved
    requests = ConciergeServiceRequest.objects.filter(status='completed', client_approval='Approved')
    return render(request, 'clientmanager/conciergerequests/completed.html', {'requests': requests})

# Denied
def concierge_denied_requests(request):
    # Only if both are denied
    requests = ConciergeServiceRequest.objects.filter(status='denied', client_approval='Denied')
    return render(request, 'clientmanager/conciergerequests/denied.html', {'requests': requests})

from django.utils.dateparse import parse_date
from django.contrib import messages

def update_concierge_request(request, request_id):
    request_obj = get_object_or_404(ConciergeServiceRequest, id=request_id)
    vendors = Vendor.objects.all()

    if request.method == 'POST':
        request_obj.status = request.POST.get('status')

        # Handle vendor
        vendor_id = request.POST.get('vendor')
        if vendor_id:
            request_obj.vendor = Vendor.objects.get(id=vendor_id)
        else:
            request_obj.vendor = None

        # Get and validate date
        date_str = request.POST.get('completation_denied_date')
        print("DEBUG: Got date:", date_str)
        parsed_date = parse_date(date_str)

        if not parsed_date:
            messages.error(request, "Completation Denied Date is required and must be valid.")
            return render(request, 'clientmanager/conciergerequests/update.html', {
                'request_obj': request_obj,
                'vendors': vendors,
            })

        request_obj.completation_denied_date = parsed_date
        request_obj.save()

        return redirect('clientmanager:concierge_open_requests')

    return render(request, 'clientmanager/conciergerequests/update.html', {
        'request_obj': request_obj,
        'vendors': vendors,
    })


# View
def view_concierge_request(request, request_id):
    request_obj = get_object_or_404(ConciergeServiceRequest, id=request_id)
    return render(request, 'clientmanager/conciergerequests/view.html', {
        'request_obj': request_obj
    })


@csrf_exempt
@require_POST
def update_concierge_cost(request):
    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        amount = data.get('amount')
        remarks = data.get('remarks', '')
        
        concierge_request = get_object_or_404(ConciergeServiceRequest, id=request_id)
        concierge_request.cost = amount
        concierge_request.cost_remarks = remarks
        concierge_request.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
def modify_concierge_approval(request):
    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        approval_status = data.get('approval_status')
        
        concierge_request = get_object_or_404(ConciergeServiceRequest, id=request_id)
        concierge_request.client_approval = approval_status
        concierge_request.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_POST
def change_concierge_status(request):
    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        status = data.get('status')
        completion_date = data.get('completion_date')
        remarks = data.get('remarks', '')
        
        concierge_request = get_object_or_404(ConciergeServiceRequest, id=request_id)
        concierge_request.status = status
        
        if completion_date:
            from datetime import datetime
            concierge_request.completation_denied_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
        
        concierge_request.status_remarks = remarks
        concierge_request.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

# Pre Arrival reqeust to client Manager ---------------------------------------------------------------------------------------------------------------
from servicedetails.models import PrearrivalInformation, Client
from django.views.decorators.http import require_http_methods
# View all requests

def clientmanager_prearrival_requests(request):
    # Show only Open status
    all_requests = PrearrivalInformation.objects.filter(status='open').order_by('-id')

    return render(request, 'clientmanager/prearrival/prearrival_list.html', {
        'requests': all_requests
    })


def clientmanager_prearrival_completed_requests(request):
    # Show only Completed status
    all_requests = PrearrivalInformation.objects.filter(status='completed').order_by('-id')

    return render(request, 'clientmanager/prearrival/prearrival_completed.html', {
        'requests': all_requests
    })


from servicedetails.models import PrearrivalInformation
@csrf_exempt
@require_http_methods(["POST"])
def upodate_prearrival_cost(request):
    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        amount = data.get('amount')
        remarks = data.get('remarks', '')
        
        prearrival_request = PrearrivalInformation.objects.get(id=request_id)
        prearrival_request.cost = int(float(amount)) if amount else 0
        prearrival_request.cost_remarks = remarks
        prearrival_request.save()
        
        return JsonResponse({'success': True})
    except PrearrivalInformation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Request not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
@csrf_exempt
@require_http_methods(["POST"])
def upodate_prearrival_approval(request):
   try:
       data = json.loads(request.body)
       request_id = data.get('request_id')
       approval_status = data.get('approval_status')
       
       prearrival_request = PrearrivalInformation.objects.get(id=request_id)
       prearrival_request.client_approval = approval_status
       
       prearrival_request.save()
       
       return JsonResponse({'success': True})
   except PrearrivalInformation.DoesNotExist:
       return JsonResponse({'success': False, 'error': 'Request not found'})
   except Exception as e:
       return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def upodate_prearrival_status(request):
   try:
       data = json.loads(request.body)
       request_id = data.get('request_id')
       status = data.get('status')
       completion_date = data.get('completion_date')
       remarks = data.get('remarks')
       
       prearrival_request = PrearrivalInformation.objects.get(id=request_id)
       prearrival_request.status = status
       prearrival_request.status_remarks = remarks
       
       # Update completation_denied_date field
       if completion_date:
           from datetime import datetime
           prearrival_request.completation_denied_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
       else:
           prearrival_request.completation_denied_date = None
       
       prearrival_request.save()
       
       return JsonResponse({'success': True})
   except PrearrivalInformation.DoesNotExist:
       return JsonResponse({'success': False, 'error': 'Request not found'})
   except ValueError as ve:
       return JsonResponse({'success': False, 'error': f'Date format error: {str(ve)}'})
   except Exception as e:
       return JsonResponse({'success': False, 'error': str(e)})
# View single request
def clientmanager_prearrival_detail(request, request_id):
    request_detail = get_object_or_404(PrearrivalInformation, id=request_id)

    if request.method == 'POST' and 'complete' in request.POST:
        request_detail.status = 'completed'
        request_detail.save()
        return redirect('clientmanager:prearrival_requests')

    return render(request, 'clientmanager/prearrival/prearrival_detail.html', {
        'request_detail': request_detail
    })


# Departure requests ---------------------------------------------------------------------------------------------------------------
# views.py

from servicedetails.models import DepartureInformation
def clientmanager_departure_requests(request):
    all_departure_requests = DepartureInformation.objects.filter(status='open').order_by('-id')

    return render(request, 'clientmanager/departure/departure_list.html', {
        'requests': all_departure_requests
    })


def clientmanager_departure_completed_requests(request):
    all_departure_requests = DepartureInformation.objects.filter(status='completed').order_by('-id')

    return render(request, 'clientmanager/departure/departure_completed_list.html', {
        'requests': all_departure_requests
    })



# Views for departure functionality

@csrf_exempt
@require_http_methods(["POST"])
def upodate_departure_cost(request):
    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        amount = data.get('amount')
        remarks = data.get('remarks', '')
        
        departure_request = DepartureInformation.objects.get(id=request_id)
        departure_request.cost = int(float(amount)) if amount else 0
        departure_request.cost_remarks = remarks
        departure_request.save()
        
        return JsonResponse({'success': True})
    except DepartureInformation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Request not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
@csrf_exempt
@require_http_methods(["POST"])
def upodate_departure_approval(request):
    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        approval_status = data.get('approval_status')
        
        departure_request = DepartureInformation.objects.get(id=request_id)
        departure_request.client_approval = approval_status
        departure_request.save()
        
        return JsonResponse({'success': True})
    except DepartureInformation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Request not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def upodate_departure_status(request):
    try:
        data = json.loads(request.body)
        request_id = data.get('request_id')
        status = data.get('status')
        completion_date = data.get('completion_date')
        remarks = data.get('remarks')
        
        departure_request = DepartureInformation.objects.get(id=request_id)
        departure_request.status = status
        departure_request.status_remarks = remarks
        
        # Update completation_denied_date field
        if completion_date:
            from datetime import datetime
            departure_request.completation_denied_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
        else:
            departure_request.completation_denied_date = None
        
        departure_request.save()
        
        return JsonResponse({'success': True})
    except DepartureInformation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Request not found'})
    except ValueError as ve:
        return JsonResponse({'success': False, 'error': f'Date format error: {str(ve)}'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def clientmanager_departure_detail(request, request_id):
    departure_request = get_object_or_404(DepartureInformation, id=request_id)

    if request.method == 'POST' and 'complete' in request.POST:
        departure_request.status = 'completed'
        departure_request.save()
        return redirect('clientmanager:departure_requests')

    return render(request, 'clientmanager/departure/departure_detail.html', {
        'request_detail': departure_request
    })

# WALK TRUG REPORTS  -------------------------------------------------------------------------------------------------------
from walkthroughreport.models import WalkthroughReport

import copy
from django.shortcuts import render, get_object_or_404

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

def all_reports_view(request):
    reports = WalkthroughReport.objects.all()
    return render(request, 'clientmanager/walkthrough/all_reports.html', {'reports': reports})

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

    return render(request, 'clientmanager/walkthrough/report_open_detail.html', {'report': filtered_report,'client_first_name': client_first_name,
        'client_last_name': client_last_name,'report_datetime': report_datetime,'report_description':report_description,'report_property':report_property}) 

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
    return render(request, 'clientmanager/walkthrough/report_detail.html', context)



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
    
    return render(request, 'clientmanager/walkthrough/open_reports.html', {'reports': processed_reports})




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
    
    return render(request, 'clientmanager/walkthrough/completed_reports.html', {'reports': processed_reports})


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
    
    return render(request, 'clientmanager/walkthrough/denied_reports.html', {'reports': processed_reports})



@require_http_methods(["GET", "POST"])
def cm_profile_update(request):
    cm_id = request.session.get("manager_id")   # ✅ FIXED
    if not cm_id:
        return redirect("mainapp:client_login")

    cm = ClientManagers.objects.get(id=cm_id)

    if request.method == "POST":
        new_username = request.POST.get("username")
        new_email = request.POST.get("email")
        new_password = request.POST.get("password")

        # ✅ Unique check against BOTH tables
        if ClientManagers.objects.exclude(id=cm.id).filter(username=new_username).exists() or \
           Client.objects.filter(username=new_username).exists():
            messages.error(request, "Username already taken.")
            return redirect("clientmanager:cm_profile_update")

        cm.username = new_username
        cm.email = new_email

        if new_password:
            cm.password = make_password(new_password)

        cm.save()
        messages.success(request, "Updated successfully.")
        return redirect("clientmanager:cm_profile_update")

    return render(request, "clientmanager/cm_profile_update.html", {"cm": cm})
