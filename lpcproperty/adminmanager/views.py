from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import AdminLoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from .models import SocialLinks, MailConfiguration
def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user and user.is_staff:
                login(request, user)
                return redirect('adminmanager:admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials or not an admin.', extra_tags='login_error')
    else:
        form = AdminLoginForm()
    return render(request, 'adminmanager/login.html', {'form': form})

# Dummy dashboard view
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    return render(request, 'adminmanager/dashboard.html')


def admin_logout(request):
    logout(request)
    return redirect('mainapp:client_login')


# Faq Section View Starts Here 
from contentpage.models import FAQ
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'adminmanager/faq/faq_list.html', {'faqs': faqs})

@login_required
@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def admin_faq_edit(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    
    if request.method == 'POST':
        faq.question = request.POST.get('question', faq.question)
        faq.answer = request.POST.get('answer', faq.answer)
        faq.category = request.POST.get('category', faq.category)
        faq.save()
        return redirect('adminmanager:admin_faq_list')

    return render(request, 'adminmanager/faq/faq_edit.html', {'faq': faq})

@login_required
@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def admin_faq_create(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        category = request.POST.get('category', 'general')

        if question and answer and category:
            FAQ.objects.create(question=question, answer=answer, category=category)
            return redirect('adminmanager:admin_faq_list')

    return render(request, 'adminmanager/faq/faq_create.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def admin_faq_delete(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    faq.delete()
    return redirect('adminmanager:admin_faq_list')

# Admin Info Statrs Here ------------------------------------------------------------------------------------------------- 
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def admin_profile(request):
    return render(request, 'adminmanager/admin/profile.html', {'admin_user': request.user})


@csrf_exempt
def edit_admin_profile(request):
    user = request.user
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        new_password = request.POST.get('password')
        if new_password:
            user.password = make_password(new_password)
        user.save()
        return redirect('adminmanager:admin_profile')

    return render(request, 'adminmanager/admin/edit_profile.html', {'admin_user': user})


@csrf_exempt
def create_admin_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and password:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=False  # change to True if you want superuser
            )
            return redirect('adminmanager:admin_profile')

    return render(request, 'adminmanager/admin/create_admin.html')

# testimonals Start Here ---------------------------------------
from contentpage.models import Testimonial

def admin_testimonial_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'adminmanager/testimonials/testimonial_list.html', {'testimonials': testimonials})

@csrf_exempt
def admin_testimonial_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        photo = request.FILES.get('photo')

        if name and comment and photo:
            Testimonial.objects.create(name=name, comment=comment, photo=photo)
            return redirect('adminmanager:testimonial_list')

    return render(request, 'adminmanager/testimonials/testimonial_create.html')


@csrf_exempt
def admin_testimonial_edit(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)

    if request.method == 'POST':
        testimonial.name = request.POST.get('name', testimonial.name)
        testimonial.comment = request.POST.get('comment', testimonial.comment)
        if request.FILES.get('photo'):
            testimonial.photo = request.FILES.get('photo')
        testimonial.save()
        return redirect('adminmanager:testimonial_list')

    return render(request, 'adminmanager/testimonials/testimonial_edit.html', {'testimonial': testimonial})


def admin_testimonial_delete(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    testimonial.delete()
    return redirect('adminmanager:testimonial_list')


# Social Links Starts Here --------------------------------------------------
from .models import SocialLinks

def social_links_list(request):
    links = SocialLinks.objects.all()
    return render(request, 'adminmanager/sociallinks/list.html', {'links': links})

@csrf_exempt
def social_links_create(request):
    if request.method == 'POST':
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        pinterest = request.POST.get('pinterest')
        linkedin = request.POST.get('linkedin')

        SocialLinks.objects.create(
            facebook=facebook,
            instagram=instagram,
            pinterest=pinterest,
            linkedin=linkedin
        )
        return redirect('adminmanager:social_links_list')

    return render(request, 'adminmanager/sociallinks/create.html')


@csrf_exempt
def social_links_edit(request, pk):
    link = get_object_or_404(SocialLinks, pk=pk)
    if request.method == 'POST':
        link.facebook = request.POST.get('facebook')
        link.instagram = request.POST.get('instagram')
        link.pinterest = request.POST.get('pinterest')
        link.linkedin = request.POST.get('linkedin')
        link.save()
        return redirect('adminmanager:social_links_list')

    return render(request, 'adminmanager/sociallinks/edit.html', {'link': link})


def social_links_delete(request, pk):
    link = get_object_or_404(SocialLinks, pk=pk)
    link.delete()
    return redirect('adminmanager:social_links_list')




# For Mail Configuration Starts Here --------------------------------------------------
from .models import MailConfiguration

def mail_config_list(request):
    configs = MailConfiguration.objects.all()
    return render(request, 'adminmanager/mailconfig/list.html', {'configs': configs})


@csrf_exempt
def mail_config_create(request):
    if request.method == 'POST':
        MailConfiguration.objects.create(
            email_host=request.POST.get('email_host'),
            email_port=request.POST.get('email_port'),
            email_host_user=request.POST.get('email_host_user'),
            email_host_password=request.POST.get('email_host_password'),
            use_tls=bool(request.POST.get('use_tls')),
            use_ssl=bool(request.POST.get('use_ssl')),
            default_from_email=request.POST.get('default_from_email')
        )
        return redirect('adminmanager:mail_config_list')

    return render(request, 'adminmanager/mailconfig/create.html')


@csrf_exempt
def mail_config_edit(request, pk):
    config = get_object_or_404(MailConfiguration, pk=pk)
    if request.method == 'POST':
        config.email_host = request.POST.get('email_host')
        config.email_port = request.POST.get('email_port')
        config.email_host_user = request.POST.get('email_host_user')
        config.email_host_password = request.POST.get('email_host_password')
        config.use_tls = bool(request.POST.get('use_tls'))
        config.use_ssl = bool(request.POST.get('use_ssl'))
        config.default_from_email = request.POST.get('default_from_email')
        config.save()
        return redirect('adminmanager:mail_config_list')

    return render(request, 'adminmanager/mailconfig/edit.html', {'config': config})


def mail_config_delete(request, pk):
    config = get_object_or_404(MailConfiguration, pk=pk)
    config.delete()
    return redirect('adminmanager:mail_config_list')

# Starts The Other works of Admin Manager  ---------------------------------------------------           START ----------------------

# Building Property  ---------------------------------------------------------------------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from propertydetails.models import PropertyManagement
from django.contrib import messages

# def get_client_manager_id(request):
#     return request.session.get('client_id')


from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
import json

def property_list_view(request):
    if request.method == "POST":
        property_id = request.POST.get("property_id")
        cm_id = request.POST.get("cm_id")

        prop = get_object_or_404(PropertyManagement, id=property_id)
        cm = get_object_or_404(ClientManagers, id=cm_id)
        prop.client_manager = cm
        prop.save()
        return redirect('adminmanager:property_list')  # change name if needed

    clients = Client.objects.all()
    properties = PropertyManagement.objects.all()
    all_cms = ClientManagers.objects.all()

    all_cms_json = json.dumps([
        {
            "id": cm.id,
            "name": f"{cm.last_name}, {cm.first_name}",
            "email": cm.email,
            "phone": cm.phone_number or cm.office_phone or ""
        } for cm in all_cms
    ], cls=DjangoJSONEncoder)

    return render(request, 'adminmanager/property/list.html', {
        'properties': properties,
        'clients': clients,
        'all_cms_json': all_cms_json
    })

from django.shortcuts import render, get_object_or_404
from propertydetails.models import PropertyManagement

def property_detail_view(request, pk):
    prop = get_object_or_404(
        PropertyManagement.objects.prefetch_related('floors__rooms'), pk=pk
    )
    return render(request, 'adminmanager/property/detail.html', {'property': prop})

from mainapp.models import Client, ClientManagers  # or whatever your models are named

from django.shortcuts import render, redirect
from propertydetails.models import PropertyManagement, Floor, Room
from mainapp.models import Client 
from django.db import transaction
from django.core.exceptions import ValidationError
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
                            return render(request, 'adminmanager/property/create.html', context)

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
                secondary_client_manager_id = request.POST.get('secondary_client_manager_id')
                
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
                        return render(request, 'adminmanager/property/create.html', context)
                    
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
                    return render(request, 'adminmanager/property/create.html', context)
                
                if not client_id:
                    error_message = "Please select or create a client"
                    context['error_message'] = error_message
                    return render(request, 'adminmanager/property/create.html', context)
                    
                if not client_manager_id:
                    error_message = "Please select or create a client manager"
                    context['error_message'] = error_message
                    return render(request, 'adminmanager/property/create.html', context)
                if secondary_client_manager_id and secondary_client_manager_id == client_manager_id:
                    context['error_message'] = "Primary and secondary client managers cannot be the same"
                    return render(request, 'adminmanager/property/create.html', context)
                # Create the Property
                prop = PropertyManagement.objects.create(
                    client_id=client_id,
                    client_manager_id=client_manager_id,
                    secondary_client_manager_id=secondary_client_manager_id or None,
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

                return redirect('adminmanager:property_list')

        except Exception as e:
            import traceback
            print("Error occurred:", str(e))
            print(traceback.format_exc())  # More detailed error for debugging
            context['error_message'] = f"Error: {str(e)}"
            return render(request, 'adminmanager/property/create.html', context)

    return render(request, 'adminmanager/property/create.html', context)



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

        return redirect('adminmanager:property_list')

    floors = prop.floors.prefetch_related('rooms').all()
    return render(request, 'adminmanager/property/edit.html', {
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

#         return redirect('adminmanager:property_list')

#     return render(request, 'adminmanager/property/edit.html', {
#         'property': prop,
#         'client_managers': client_managers
#     })



from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.conf import settings
import os
from django.shortcuts import get_object_or_404

def property_delete_view(request, pk):
    prop = get_object_or_404(PropertyManagement, pk=pk)

    if request.method == 'POST':
        prop.delete()
        return redirect('adminmanager:property_list')

    return render(request, 'adminmanager/property/delete.html', {'property': prop})

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


# Building Services  ---------------------------------------------------------------------------------------------------------------
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
    
    return render(request, 'adminmanager/vendor/list.html', {'vendors': vendors})

import uuid
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from mainapp.models import Vendor
import uuid
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from mainapp.models import Vendor, VendorContact
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

        return redirect('adminmanager:vendor_list')

    # Get services from database
    vendor_services = VendorServices.objects.all().order_by('service')

    context = {
        'vendor_services': vendor_services,
        'US_STATES': US_STATES,
    }

    return render(request, 'adminmanager/vendor/create.html', context)

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

        return redirect('adminmanager:vendor_list')

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

    return render(request, 'adminmanager/vendor/edit.html', context)
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

    return render(request, 'adminmanager/vendor/details.html', context)

# Delete vendor
def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.delete()
    return redirect('adminmanager:vendor_list')

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
    return render(request, 'adminmanager/vendor/manage.html', context)

# Client Manager Profile Update ---------------------------------------------------------------------------------------------------------------   
from django.shortcuts import render, redirect, get_object_or_404
from mainapp.models import ClientManagers

def clientmanager_profile_view(request):
    clientmanagers = ClientManagers.objects.all()
    return render(request, 'clientmanager/profile/clientmanager_profile_view.html', {
        'clientmanagers': clientmanagers
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
        'contact_choices': ClientManagers.PREFERRED_CONTACT_CHOICES,
        
    })


# Pre Arrival reqeust to client Manager ---------------------------------------------------------------------------------------------------------------
from servicedetails.models import PrearrivalInformation, Client
from django.views.decorators.http import require_http_methods
# View all requests

def clientmanager_prearrival_requests(request):
    # Show only Open status
    all_requests = PrearrivalInformation.objects.filter(status='open').order_by('-id')

    return render(request, 'adminmanager/prearrival/prearrival_list.html', {
        'requests': all_requests
    })


def clientmanager_prearrival_completed_requests(request):
    # Show only Completed status
    all_requests = PrearrivalInformation.objects.filter(status='completed').order_by('-id')

    return render(request, 'adminmanager/prearrival/prearrival_completed.html', {
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
        return redirect('adminmanager:prearrival_requests')

    return render(request, 'adminmanager/prearrival/prearrival_detail.html', {
        'request_detail': request_detail
    })


# Departure requests ---------------------------------------------------------------------------------------------------------------
# views.py

from servicedetails.models import DepartureInformation
def clientmanager_departure_requests(request):
    all_departure_requests = DepartureInformation.objects.filter(status='open').order_by('-id')

    return render(request, 'adminmanager/departure/departure_list.html', {
        'requests': all_departure_requests
    })


def clientmanager_departure_completed_requests(request):
    all_departure_requests = DepartureInformation.objects.filter(status='completed').order_by('-id')

    return render(request, 'adminmanager/departure/departure_completed_list.html', {
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
        return redirect('adminmanager:departure_requests')

    return render(request, 'adminmanager/departure/departure_detail.html', {
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
    requests = ServiceRequest.objects.filter(status='pending')
    return render(request, 'adminmanager/servicerequests/pending.html', {'requests': requests})

from django.db.models import Q

def open_requests(request):
    # Show all except if both are approved and completed OR both are denied
    requests = ServiceRequest.objects.exclude(
        Q(status='completed', client_approval='Approved') |
        Q(status='denied', client_approval='Denied')
    )
    return render(request, 'adminmanager/servicerequests/open.html', {'requests': requests})

def completed_requests(request):
    # Only if both are completed and approved
    requests = ServiceRequest.objects.filter(status='completed', client_approval='Approved')
    return render(request, 'adminmanager/servicerequests/completed.html', {'requests': requests})

def denied_requests(request):
    # Only if both are denied
    requests = ServiceRequest.objects.filter(status='denied', client_approval='Denied')
    return render(request, 'adminmanager/servicerequests/denied.html', {'requests': requests})

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
            return render(request, 'adminmanager/servicerequests/update.html', {
                'request_obj': request_obj,
                'vendors': vendors,
            })

        request_obj.completation_denied_date = parsed_date
        request_obj.save()

        return redirect('adminmanager:clientmanager_open_requests')

    return render(request, 'adminmanager/servicerequests/update.html', {
        'request_obj': request_obj,
        'vendors': vendors,
    })


def service_request_detail(request, request_id):
    request_obj = get_object_or_404(ServiceRequest, id=request_id)

    return render(request, 'adminmanager/servicerequests/detail_view.html', {
        'request_obj': request_obj
    })

# Congiure Request ----------------------------------------------------------------------------------------------------------------------
from servicedetails.models import ConciergeServiceRequest

# Pending
def concierge_pending_requests(request):
    requests = ConciergeServiceRequest.objects.filter(status='pending')
    return render(request, 'adminmanager/conciergerequests/pending.html', {'requests': requests})

from django.db.models import Q

# Open
def concierge_open_requests(request):
    # Show all except if both are approved and completed OR both are denied
    requests = ConciergeServiceRequest.objects.exclude(
        Q(status='completed', client_approval='Approved') |
        Q(status='denied', client_approval='Denied')
    )
    return render(request, 'adminmanager/conciergerequests/open.html', {'requests': requests})

# Completed
def concierge_completed_requests(request):
    # Only if both are completed and approved
    requests = ConciergeServiceRequest.objects.filter(status='completed', client_approval='Approved')
    return render(request, 'adminmanager/conciergerequests/completed.html', {'requests': requests})

# Denied
def concierge_denied_requests(request):
    # Only if both are denied
    requests = ConciergeServiceRequest.objects.filter(status='denied', client_approval='Denied')
    return render(request, 'adminmanager/conciergerequests/denied.html', {'requests': requests})

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
            return render(request, 'adminmanager/conciergerequests/update.html', {
                'request_obj': request_obj,
                'vendors': vendors,
            })

        request_obj.completation_denied_date = parsed_date
        request_obj.save()

        return redirect('adminmanager:concierge_open_requests')

    return render(request, 'adminmanager/conciergerequests/update.html', {
        'request_obj': request_obj,
        'vendors': vendors,
    })


# View
def view_concierge_request(request, request_id):
    request_obj = get_object_or_404(ConciergeServiceRequest, id=request_id)
    return render(request, 'adminmanager/conciergerequests/view.html', {
        'request_obj': request_obj
    })


# property Improvement Request ---------------------------------------------------------------------------------------------------------------
from propertydetails.models import PropertyImprovement

# Pending
def property_pending_requests(request):
    requests = PropertyImprovement.objects.filter(status='pending')
    return render(request, 'adminmanager/propertyimprovement/pending.html', {'requests': requests})

# Open
def property_open_requests(request):
    requests = PropertyImprovement.objects.filter(status='open')
    return render(request, 'adminmanager/propertyimprovement/open.html', {'requests': requests})

# Completed
def property_completed_requests(request):
    requests = PropertyImprovement.objects.filter(status='completed')
    return render(request, 'adminmanager/propertyimprovement/completed.html', {'requests': requests})

# Denied
def property_denied_requests(request):
    requests = PropertyImprovement.objects.filter(status='denied')
    return render(request, 'adminmanager/propertyimprovement/denied.html', {'requests': requests})

# Update
def update_property_request(request, request_id):
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
        return redirect('adminmanager:property_pending_requests')

    return render(request, 'adminmanager/propertyimprovement/update.html', {
        'request_obj': request_obj,
        'vendors': vendors,
    })

# View
def view_property_request(request, request_id):
    request_obj = get_object_or_404(PropertyImprovement, id=request_id)
    return render(request, 'adminmanager/propertyimprovement/view.html', {
        'request_obj': request_obj
    })


# Building WALKTHROUGH REPORT ------------------------------------------------------------------------------------------
from django.shortcuts import render
from django.http import HttpResponse
from walkthroughreport.models import WalkthroughReport
from mainapp.models import Client
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.shortcuts import render, redirect
from walkthroughreport.forms import (
    WalkthroughReportForm,
    GeneralItemsExteriorForm,
    GeneralItemsInteriorForm,
    GarageForm,
    LaundryForm,
    KitchenForm,
    ButlersForm,
    BreakfastAreaForm,
    EntryFoyerForm,
    GreatRoomForm,
    DiningRoomForm,
    ClosetsMainLevelForm,
    ClosetsUpperLevelForm,
    HallwaysMainLevelForm,
    HallwaysUpperLevelForm,
    Bedroom1Form, Bedroom2Form, Bedroom3Form, Bedroom4Form, Bedroom5Form,
    Bedroom6Form, Bedroom7Form, Bedroom8Form, Bedroom9Form, Bedroom10Form,
    Bathroom1Form, Bathroom2Form, Bathroom3Form, Bathroom4Form, Bathroom5Form,
    Bathroom6Form, Bathroom7Form, Bathroom8Form, Bathroom9Form, Bathroom10Form,
    Bathroom11Form, Bathroom12Form,
    GymForm,
    TheatreMusicRoomForm,
    GuestHouseSleepingForm,
    GuestHouseBathForm
)

def process_form_data(post_data):
    """Clean POST data to handle empty amount fields"""
    cleaned_data = post_data.copy()
    for key, value in cleaned_data.items():
        if 'amount' in key and (value == '' or value is None):
            cleaned_data[key] = '0'
    return cleaned_data

def walkthrough_report_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Admin is logged in
        base_template = 'adminmanager/dashboardbase.html'
    elif 'manager_id' in request.session:
        # Client manager is logged in
        base_template = 'clientmanager/managerbase.html'
    else:
        # Default fallback (or client)
        base_template = 'adminmanager/dashboardbase.html'
    if request.method == 'POST':
        # Clean the POST data
        cleaned_post_data = process_form_data(request.POST)
        
        # Initialize all forms with cleaned POST data
        report_form = WalkthroughReportForm(cleaned_post_data)
        exterior_form = GeneralItemsExteriorForm(cleaned_post_data)
        interior_form = GeneralItemsInteriorForm(cleaned_post_data)
        garage_form = GarageForm(cleaned_post_data)
        laundry_form = LaundryForm(cleaned_post_data)
        kitchen_form = KitchenForm(cleaned_post_data)
        butlers_form = ButlersForm(cleaned_post_data)
        breakfast_area_form = BreakfastAreaForm(cleaned_post_data)
        entry_foyer_form = EntryFoyerForm(cleaned_post_data)
        great_room_form = GreatRoomForm(cleaned_post_data)
        dining_room_form = DiningRoomForm(cleaned_post_data)
        closets_main_level_form = ClosetsMainLevelForm(cleaned_post_data)
        closets_upper_level_form = ClosetsUpperLevelForm(cleaned_post_data)
        hallways_main_level_form = HallwaysMainLevelForm(cleaned_post_data)
        hallways_upper_level_form = HallwaysUpperLevelForm(cleaned_post_data)
        
        # Bedroom forms
        bedroom1_form = Bedroom1Form(cleaned_post_data)
        bedroom2_form = Bedroom2Form(cleaned_post_data)
        bedroom3_form = Bedroom3Form(cleaned_post_data)
        bedroom4_form = Bedroom4Form(cleaned_post_data)
        bedroom5_form = Bedroom5Form(cleaned_post_data)
        bedroom6_form = Bedroom6Form(cleaned_post_data)
        bedroom7_form = Bedroom7Form(cleaned_post_data)
        bedroom8_form = Bedroom8Form(cleaned_post_data)
        bedroom9_form = Bedroom9Form(cleaned_post_data)
        bedroom10_form = Bedroom10Form(cleaned_post_data)
        
        # Bathroom forms
        bathroom1_form = Bathroom1Form(cleaned_post_data)
        bathroom2_form = Bathroom2Form(cleaned_post_data)
        bathroom3_form = Bathroom3Form(cleaned_post_data)
        bathroom4_form = Bathroom4Form(cleaned_post_data)
        bathroom5_form = Bathroom5Form(cleaned_post_data)
        bathroom6_form = Bathroom6Form(cleaned_post_data)
        bathroom7_form = Bathroom7Form(cleaned_post_data)
        bathroom8_form = Bathroom8Form(cleaned_post_data)
        bathroom9_form = Bathroom9Form(cleaned_post_data)
        bathroom10_form = Bathroom10Form(cleaned_post_data)
        bathroom11_form = Bathroom11Form(cleaned_post_data)
        bathroom12_form = Bathroom12Form(cleaned_post_data)
        
        # Additional forms
        gym_form = GymForm(cleaned_post_data)
        theatre_music_room_form = TheatreMusicRoomForm(cleaned_post_data)
        guest_house_sleeping_form = GuestHouseSleepingForm(cleaned_post_data)
        guest_house_bath_form = GuestHouseBathForm(cleaned_post_data)

        # Collect all forms for validation
        all_forms = [
            report_form, exterior_form, interior_form, garage_form, laundry_form,
            kitchen_form, butlers_form, breakfast_area_form, entry_foyer_form,
            great_room_form, dining_room_form, closets_main_level_form,
            closets_upper_level_form, hallways_main_level_form, hallways_upper_level_form,
            bedroom1_form, bedroom2_form, bedroom3_form, bedroom4_form, bedroom5_form,
            bedroom6_form, bedroom7_form, bedroom8_form, bedroom9_form, bedroom10_form,
            bathroom1_form, bathroom2_form, bathroom3_form, bathroom4_form, bathroom5_form,
            bathroom6_form, bathroom7_form, bathroom8_form, bathroom9_form, bathroom10_form,
            bathroom11_form, bathroom12_form, gym_form, theatre_music_room_form,
            guest_house_sleeping_form, guest_house_bath_form
        ]

        # Debug: Print validation errors
        invalid_forms = []
        for i, form in enumerate(all_forms):
            if not form.is_valid():
                invalid_forms.append((i, form.__class__.__name__, form.errors))
        
        if invalid_forms:
            print("Invalid forms:")
            for i, name, errors in invalid_forms:
                print(f"{name}: {errors}")

        # Check if all forms are valid
        if all(form.is_valid() for form in all_forms):
            # Save the main report first
            report_instance = report_form.save()

            # Save all related forms
            forms_to_save = [
                (exterior_form, 'general_items_exterior'),
                (interior_form, 'general_items_interior'),
                (garage_form, 'garage'),
                (laundry_form, 'laundry'),
                (kitchen_form, 'kitchen'),
                (butlers_form, 'butlers'),
                (breakfast_area_form, 'breakfast_area'),
                (entry_foyer_form, 'entry_foyer'),
                (great_room_form, 'great_room'),
                (dining_room_form, 'dining_room'),
                (closets_main_level_form, 'closets_main_level'),
                (closets_upper_level_form, 'closets_upper_level'),
                (hallways_main_level_form, 'hallways_main_level'),
                (hallways_upper_level_form, 'hallways_upper_level'),
                (bedroom1_form, 'bedroom1'),
                (bedroom2_form, 'bedroom2'),
                (bedroom3_form, 'bedroom3'),
                (bedroom4_form, 'bedroom4'),
                (bedroom5_form, 'bedroom5'),
                (bedroom6_form, 'bedroom6'),
                (bedroom7_form, 'bedroom7'),
                (bedroom8_form, 'bedroom8'),
                (bedroom9_form, 'bedroom9'),
                (bedroom10_form, 'bedroom10'),
                (bathroom1_form, 'bathroom1'),
                (bathroom2_form, 'bathroom2'),
                (bathroom3_form, 'bathroom3'),
                (bathroom4_form, 'bathroom4'),
                (bathroom5_form, 'bathroom5'),
                (bathroom6_form, 'bathroom6'),
                (bathroom7_form, 'bathroom7'),
                (bathroom8_form, 'bathroom8'),
                (bathroom9_form, 'bathroom9'),
                (bathroom10_form, 'bathroom10'),
                (bathroom11_form, 'bathroom11'),
                (bathroom12_form, 'bathroom12'),
                (gym_form, 'gym'),
                (theatre_music_room_form, 'theatre_music_room'),
                (guest_house_sleeping_form, 'guest_house_sleeping_living'),
                (guest_house_bath_form, 'guest_house_bathroom')
            ]

            for form, relation_name in forms_to_save:
                instance = form.save(commit=False)
                instance.walkthrough_report = report_instance
                instance.save()

            return redirect('adminmanager:walkthrough-success')
        else:
            # Re-render form with errors
            pass

    else:
        # Initialize all forms for GET request
        report_form = WalkthroughReportForm()
        exterior_form = GeneralItemsExteriorForm()
        interior_form = GeneralItemsInteriorForm()
        garage_form = GarageForm()
        laundry_form = LaundryForm()
        kitchen_form = KitchenForm()
        butlers_form = ButlersForm()
        breakfast_area_form = BreakfastAreaForm()
        entry_foyer_form = EntryFoyerForm()
        great_room_form = GreatRoomForm()
        dining_room_form = DiningRoomForm()
        closets_main_level_form = ClosetsMainLevelForm()
        closets_upper_level_form = ClosetsUpperLevelForm()
        hallways_main_level_form = HallwaysMainLevelForm()
        hallways_upper_level_form = HallwaysUpperLevelForm()
        
        # Bedroom forms
        bedroom1_form = Bedroom1Form()
        bedroom2_form = Bedroom2Form()
        bedroom3_form = Bedroom3Form()
        bedroom4_form = Bedroom4Form()
        bedroom5_form = Bedroom5Form()
        bedroom6_form = Bedroom6Form()
        bedroom7_form = Bedroom7Form()
        bedroom8_form = Bedroom8Form()
        bedroom9_form = Bedroom9Form()
        bedroom10_form = Bedroom10Form()
        
        # Bathroom forms
        bathroom1_form = Bathroom1Form()
        bathroom2_form = Bathroom2Form()
        bathroom3_form = Bathroom3Form()
        bathroom4_form = Bathroom4Form()
        bathroom5_form = Bathroom5Form()
        bathroom6_form = Bathroom6Form()
        bathroom7_form = Bathroom7Form()
        bathroom8_form = Bathroom8Form()
        bathroom9_form = Bathroom9Form()
        bathroom10_form = Bathroom10Form()
        bathroom11_form = Bathroom11Form()
        bathroom12_form = Bathroom12Form()
        
        # Additional forms
        gym_form = GymForm()
        theatre_music_room_form = TheatreMusicRoomForm()
        guest_house_sleeping_form = GuestHouseSleepingForm()
        guest_house_bath_form = GuestHouseBathForm()

    return render(request, 'walkthrough_form.html', {
        'base_template': base_template,
        'form': report_form,
        'exterior_form': exterior_form,
        'interior_form': interior_form,
        'garage_form': garage_form,
        'laundry_form': laundry_form,
        'kitchen_form': kitchen_form,
        'butlers_form': butlers_form,
        'breakfast_area_form': breakfast_area_form,
        'entry_foyer_form': entry_foyer_form,
        'great_room_form': great_room_form,
        'dining_room_form': dining_room_form,
        'closets_main_level_form': closets_main_level_form,
        'closets_upper_level_form': closets_upper_level_form,
        'hallways_main_level_form': hallways_main_level_form,
        'hallways_upper_level_form': hallways_upper_level_form,
        'bedroom1_form': bedroom1_form,
        'bedroom2_form': bedroom2_form,
        'bedroom3_form': bedroom3_form,
        'bedroom4_form': bedroom4_form,
        'bedroom5_form': bedroom5_form,
        'bedroom6_form': bedroom6_form,
        'bedroom7_form': bedroom7_form,
        'bedroom8_form': bedroom8_form,
        'bedroom9_form': bedroom9_form,
        'bedroom10_form': bedroom10_form,
        'bathroom1_form': bathroom1_form,
        'bathroom2_form': bathroom2_form,
        'bathroom3_form': bathroom3_form,
        'bathroom4_form': bathroom4_form,
        'bathroom5_form': bathroom5_form,
        'bathroom6_form': bathroom6_form,
        'bathroom7_form': bathroom7_form,
        'bathroom8_form': bathroom8_form,
        'bathroom9_form': bathroom9_form,
        'bathroom10_form': bathroom10_form,
        'bathroom11_form': bathroom11_form,
        'bathroom12_form': bathroom12_form,
        'gym_form': gym_form,
        'theatre_music_room_form': theatre_music_room_form,
        'guest_house_sleeping_form': guest_house_sleeping_form,
        'guest_house_bath_form': guest_house_bath_form,
    })



def walkthrough_success_view(request):
    return render(request, 'walkthrough_success.html')

# walkthrough report Done ------------------------------------------------------------------------------------------------------------------

# Client Management 
from django.shortcuts import render, get_object_or_404, redirect
from mainapp.models import Client

def client_list_page(request):
    clients = Client.objects.all()
    return render(request, 'adminmanager/client/client_list_page.html', {'clients': clients})

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
        client.contact1_last_name  = request.POST.get('contact1_last_name')
        client.contact1_email = request.POST.get('contact1_email')
        client.contact1_phone = request.POST.get('contact1_phone')
        client.contact1_preferred = request.POST.get('contact1_preferred')

        client.contact2_name = request.POST.get('contact2_name')
        client.contact2_last_name  = request.POST.get('contact2_last_name')
        client.contact2_email = request.POST.get('contact2_email')
        client.contact2_phone = request.POST.get('contact2_phone')
        client.contact2_preferred = request.POST.get('contact2_preferred')

        client.contact3_name = request.POST.get('contact3_name')
        client.contact3_last_name  = request.POST.get('contact3_last_name')
        client.contact3_email = request.POST.get('contact3_email')
        client.contact3_phone = request.POST.get('contact3_phone')
        client.contact3_preferred = request.POST.get('contact3_preferred')

        client.save()
        return redirect('adminmanager:client_list_page')

    return render(request, 'adminmanager/client/client_edit_page.html', {'client': client})

from django.db import IntegrityError
def create_new_client_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Check for existing username/email
        if Client.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different username."
        elif Client.objects.filter(email=email).exists():
            error_message = "Email already exists. Please use a different email."
        else:
            try:
                Client.objects.create(
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    username=username,
                    email=email,
                    password=request.POST.get('password'),
                    address=request.POST.get('address'),
                    city=request.POST.get('city'),
                    state=request.POST.get('state'),
                    zipcode=request.POST.get('zipcode'),
                    phone_number=request.POST.get('phone_number'),
                    preferred_contact_method=request.POST.get('preferred_contact_method'),

                    # Contact 1
                    contact1_name=request.POST.get('contact1_name'),
                    contact1_last_name=request.POST.get('contact1_last_name'),
                    contact1_email=request.POST.get('contact1_email'),
                    contact1_phone=request.POST.get('contact1_phone'),
                    contact1_preferred=request.POST.get('contact1_preferred'),

                    # Contact 2
                    contact2_name=request.POST.get('contact2_name'),
                    contact2_last_name=request.POST.get('contact2_last_name'),
                    contact2_email=request.POST.get('contact2_email'),
                    contact2_phone=request.POST.get('contact2_phone'),
                    contact2_preferred=request.POST.get('contact2_preferred'),

                    # Contact 3
                    contact3_name=request.POST.get('contact3_name'),
                    contact3_last_name=request.POST.get('contact3_last_name'),
                    contact3_email=request.POST.get('contact3_email'),
                    contact3_phone=request.POST.get('contact3_phone'),
                    contact3_preferred=request.POST.get('contact3_preferred'),
                )
                return redirect('adminmanager:client_list_page')

            except IntegrityError as e:
                error_message = "An unexpected error occurred. Please try again."

    return render(request, 'adminmanager/client/create.html', {
        'error_message': error_message
    })

# Client Manager Things Update ---------------------------------------------------------------------------------------------------------------
from django.shortcuts import render, get_object_or_404, redirect
from mainapp.models import ClientManagers
from django.contrib import messages

# List View
def clientmanager_list_view(request):
    clientmanagers = ClientManagers.objects.all()
    return render(request, 'adminmanager/clientmanager/clientmanager_list.html', {'clientmanagers': clientmanagers})

# Detail View
def clientmanager_detail_view(request, pk):
    clientmanager = get_object_or_404(ClientManagers, pk=pk)
    return render(request, 'adminmanager/clientmanager/clientmanager_detail.html', {'clientmanager': clientmanager})

from django.core.mail import EmailMultiAlternatives
def clientmanager_create_view(request):
    if request.method == 'POST':
        data = request.POST
        password = data.get('password')

        # Create Client Manager
        cm = ClientManagers(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('username'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            city=data.get('city'),
            state=data.get('state'),
            zipcode=data.get('zipcode'),
            office_phone=data.get('office_phone'),
            preferred_contact_method=data.get('preferred_contact_method'),
        )
        cm.set_password(password)
        cm.save()

        # Send Welcome Email (simple professional HTML)
        subject = "Welcome to LPC Properties"
        message = f"""
Hello {cm.first_name},

Welcome to LPC Properties!

Your account has been successfully created.

You can log in here:
https://backend.lotuspmc.com/login/

Your credentials are:
Username: {cm.username}
Password: {password}

Please keep this information safe.

Best regards,
LPC Properties Team
        """.strip()

        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 30px;">
            <div style="max-width: 600px; margin: auto; background: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px;">
                <div style="background-color: #004aad; color: white; padding: 15px 25px; border-radius: 8px 8px 0 0;">
                    <h2 style="margin: 0;">Welcome to LPC Properties</h2>
                </div>
                <div style="padding: 25px; color: #333;">
                    <p>Hi <strong>{cm.first_name}</strong>,</p>
                    <p>Welcome to <strong>LPC Properties</strong>! Your account has been created successfully.</p>
                    <p>Here are your login credentials:</p>
                    <div style="background-color: #f4f4f4; padding: 15px; border-radius: 6px; border: 1px solid #ddd;">
                        <p><strong>Username:</strong> {cm.username}</p>
                        <p><strong>Password:</strong> {password}</p>
                    </div>
                    <p style="margin-top: 20px;">You can log in using the link below:</p>
                    <a href="https://backend.lotuspmc.com/login/" 
                       style="display: inline-block; background-color: #004aad; color: white; text-decoration: none; padding: 10px 20px; border-radius: 5px; margin-top: 10px;">
                       Log In to Your Account
                    </a>
                    <p style="margin-top: 25px;">Please keep this information safe.</p>
                    <p>Best regards,<br><strong>LPC Properties Team</strong></p>
                </div>
            </div>
        </body>
        </html>
        """

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [cm.email],
                fail_silently=False,
                html_message=html_message,
            )
        except Exception as e:
            messages.warning(request, f"Client Manager created, but failed to send email: {e}")

        messages.success(request, "Client Manager created successfully and credentials sent via email.")
        return redirect('adminmanager:list')

    return render(request, 'adminmanager/clientmanager/clientmanager_form.html', {
        'action': 'Create',
        'contact_choices': ClientManagers.PREFERRED_CONTACT_CHOICES,
        'US_STATES': US_STATES,
    })


US_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]
# Edit View
def clientmanager_edit_view(request, pk):
    cm = get_object_or_404(ClientManagers, pk=pk)

    if request.method == 'POST':
        data = request.POST
        cm.first_name = data.get('first_name')
        cm.last_name = data.get('last_name')
        cm.username = data.get('username')
        cm.email = data.get('email')
        cm.phone_number = data.get('phone_number')
        cm.city = data.get('city')
        cm.state = data.get('state')
        cm.zipcode = data.get('zipcode')
        cm.office_phone = data.get('office_phone')  # ✅ fixed — removed comma
        cm.preferred_contact_method = data.get('preferred_contact_method')

        if data.get('password'):
            cm.set_password(data.get('password'))

        cm.save()
        messages.success(request, "Client Manager updated successfully.")
        return redirect('adminmanager:list')

    return render(request, 'adminmanager/clientmanager/clientmanager_edit.html', {
        'clientmanager': cm,
        'action': 'Edit',
        'contact_choices': ClientManagers.PREFERRED_CONTACT_CHOICES,
        'US_STATES': US_STATES,
    })


# Delete View
def clientmanager_delete_view(request, pk):
    cm = get_object_or_404(ClientManagers, pk=pk)
    if request.method == 'POST':
        cm.delete()
        messages.success(request, "Client Manager deleted successfully.")
        return redirect('adminmanager:list')
    return render(request, 'adminmanager/clientmanager/clientmanager_confirm_delete.html', {'clientmanager': cm})

from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.mail import EmailMessage, get_connection
from adminmanager.mail_config import get_mail_settings  # adjust 'core' to your app name
from django.http import HttpResponse

@csrf_exempt
def send_email_view(request):
    if request.method == 'POST':
        to_email = request.POST.get('to_email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        mail_settings = get_mail_settings()
        if not mail_settings:
            return render(request, 'adminmanager/success/success_mail.html', {'status': 'error', 'message': 'Email configuration missing!'})

        try:
            # Create a custom email connection
            connection = get_connection(
                backend=mail_settings['EMAIL_BACKEND'],
                host=mail_settings['EMAIL_HOST'],
                port=mail_settings['EMAIL_PORT'],
                username=mail_settings['EMAIL_HOST_USER'],
                password=mail_settings['EMAIL_HOST_PASSWORD'],
                use_tls=mail_settings['EMAIL_USE_TLS'],
                use_ssl=mail_settings['EMAIL_USE_SSL'],
            )

            email = EmailMessage(
                subject,
                message,
                mail_settings['DEFAULT_FROM_EMAIL'],
                [to_email],
                connection=connection,  # important fix
            )
            email.fail_silently = False
            email.send()

            return render(request, 'adminmanager/success/success_mail.html', {'status': 'success', 'message': 'Email sent successfully!'})
        except Exception as e:
            # Directly show the error without template
            return HttpResponse(f"Failed to send email: {str(e)}", status=500)


# services updates html -------------------------------------------------------------------------------------

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from servicedetails.models import ServiceRequest

@csrf_exempt
def update_cost(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            req = ServiceRequest.objects.get(id=data['id'])
            req.cost = data['cost']
            req.save()
            return JsonResponse({'success': True})
        except ServiceRequest.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Request not found'})
    return JsonResponse({'success': False, 'error': 'Invalid method'})


from servicedetails.models import ConciergeServiceRequest

@csrf_exempt
def update_concierge_cost(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            req = ConciergeServiceRequest.objects.get(id=data['id'])
            req.cost = data['cost']
            req.save()
            return JsonResponse({'success': True})
        except ConciergeServiceRequest.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Request not found'})
    return JsonResponse({'success': False, 'error': 'Invalid method'})


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
    
# for email send to contact purpose only ---------------------------------------------------------------------------------
# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail, get_connection
from django.views.decorators.http import require_POST
import json

from adminmanager.models import MailConfiguration


@require_POST
def send_contact_email(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        subject = data.get('subject')
        content = data.get('content')
        
        # Fetch mail configuration
        mail_config = MailConfiguration.objects.first()
        
        if not mail_config:
            return JsonResponse({'success': False, 'error': 'Mail configuration not found'})
        
        # Create email connection with configuration from database
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=mail_config.email_host,
            port=mail_config.email_port,
            username=mail_config.email_host_user,
            password=mail_config.email_host_password,
            use_tls=mail_config.use_tls,
            use_ssl=mail_config.use_ssl,
        )
        
        send_mail(
            subject,
            content,
            mail_config.default_from_email,
            [email],
            fail_silently=False,
            connection=connection,
        )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    


# To SEND SMS using SlickText API -------------------------------------------------------------------------------------------------
# In your views.py, add this import at the top
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os

# Add the parent directory to Python path to import sms_service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sms_service import SlickTextSMSService

# Add this new view
@csrf_exempt
@require_http_methods(["POST"])
def send_sms_view(request):
    try:
        data = json.loads(request.body)
        phone_number = data.get('phone_number', '').strip()
        message = data.get('message', '').strip()

        if not phone_number:
            return JsonResponse({
                'success': False,
                'error': 'Phone number is required'
            }, status=400)

        if not message:
            return JsonResponse({
                'success': False,
                'error': 'Message is required'
            }, status=400)

        # Append automated disclaimer
        disclaimer = (
            "\n\nThis is an automated message. Replies to this number are not monitored. "
            "If you need assistance, please contact us at (561) 766-7828 or visit https://lotuspmc.com"
        )
        full_message = f"{message}{disclaimer}"

        # Send SMS
        sms_service = SlickTextSMSService()
        result = sms_service.send_sms(phone_number, full_message)

        if result.get('success'):
            return JsonResponse({
                'success': True,
                'message': 'SMS sent successfully!'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result.get('error', 'Failed to send SMS')
            }, status=400)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)