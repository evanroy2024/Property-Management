from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import AdminLoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout

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

        if question and answer:
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


def property_list_view(request):
    clients = Client.objects.all()
    properties = PropertyManagement.objects.all()  # Removed filtering
    return render(request, 'adminmanager/property/list.html', {'properties': properties,'clients': clients})
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
                client_id = request.POST.get('client_id')
                
                # If no existing client selected, try creating a new one
                if not client_id:
                    new_first_name = request.POST.get('new_first_name', '')
                    new_last_name = request.POST.get('new_last_name', '')
                    new_username = request.POST.get('new_username', '')
                    new_email = request.POST.get('new_email', '')
                    new_password = request.POST.get('new_password', '')
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
                        if not all([new_first_name, new_last_name, new_username, new_email, new_password]):
                            error_message = "Please complete all required fields for the new client"
                            context['error_message'] = error_message
                            return render(request, 'adminmanager/property/create.html', context)

                        # Create new client
                        new_client = Client.objects.create(
                            first_name=new_first_name,
                            last_name=new_last_name,
                            username=new_username,
                            email=new_email,
                            password=new_password,
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

def property_update_view(request, pk):
    prop = get_object_or_404(PropertyManagement, pk=pk)
    client = prop.client
    client_managers = ClientManagers.objects.all()

    if request.method == 'POST':
        # Handling Property and Client Info Updates
        if 'address' in request.POST:
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
from mainapp.models import Vendor

# List vendors
def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'adminmanager/vendor/list.html', {'vendors': vendors})


import uuid  # For generating a unique string
from mainapp.models import VendorService
def create_vendor(request):
    # Get all services for the dropdown
    all_services = VendorService.objects.all().order_by('name')
    
    if request.method == 'POST':
        # Get selected services and additional services
        selected_services = request.POST.getlist('service[]')
        additional_service = request.POST.get('additional_service', '')
        
        combined_services = selected_services
        
        # Process additional services
        if additional_service:
            additional_list = [s.strip() for s in additional_service.split(',') if s.strip()]
            
            # Add new services to the VendorService model
            for service_name in additional_list:
                if service_name:
                    VendorService.objects.get_or_create(name=service_name)
            
            combined_services += additional_list
        
        # Auto-generate a dummy username
        auto_username = f'vendor_{uuid.uuid4().hex[:6]}'
        
        Vendor.objects.create(
            company_name=request.POST.get('company_name'),
            username=auto_username,
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone_number'),
            service=', '.join(combined_services),
        )
        return redirect('adminmanager:vendor_list')
    
    # Pass all services to the template
    return render(request, 'adminmanager/vendor/create.html', {
        'service_choices': [(service.name, service.name) for service in all_services]
    })
# Edit vendor
def edit_vendor(request, vendor_id):
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

        # Get selected services and additional services
        selected_services = request.POST.getlist('service[]')
        additional_service = request.POST.get('additional_service', '')

        # Combine them into one string, if you're storing as comma-separated
        combined_services = selected_services
        if additional_service:
            additional_list = [s.strip() for s in additional_service.split(',') if s.strip()]
            
            # Add new services to the VendorService model
            for service_name in additional_list:
                if service_name:
                    VendorService.objects.get_or_create(name=service_name)
                    
            combined_services += additional_list

        # Save combined service string (e.g. comma-separated)
        vendor.service = ', '.join(combined_services)
        vendor.save()

        return redirect('adminmanager:vendor_list')

    # Prepare existing services for form pre-checking
    existing_services = [s.strip() for s in vendor.service.split(',')] if vendor.service else []

    # Get all services for the dropdown
    all_services = VendorService.objects.all().order_by('name')

    context = {
        'vendor': vendor,
        'selected_services': existing_services,
        'service_choices': [(service.name, service.name) for service in all_services],
    }

    return render(request, 'adminmanager/vendor/edit.html', context)

# Delete vendor
def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.delete()
    return redirect('adminmanager:vendor_list')


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
        'contact_choices': ClientManagers.PREFERRED_CONTACT_CHOICES
    })


# Pre Arrival reqeust to client Manager ---------------------------------------------------------------------------------------------------------------
from servicedetails.models import PrearrivalInformation, Client

# View all requests

def clientmanager_prearrival_requests(request):
    all_requests = PrearrivalInformation.objects.all().order_by('-id')

    return render(request, 'adminmanager/prearrival/prearrival_list.html', {
        'requests': all_requests
    })

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
    all_departure_requests = DepartureInformation.objects.all().order_by('-id')

    return render(request, 'adminmanager/departure/departure_list.html', {
        'requests': all_departure_requests
    })
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

def open_requests(request):
    requests = ServiceRequest.objects.filter(status='open')
    return render(request, 'adminmanager/servicerequests/open.html', {'requests': requests})

def completed_requests(request):
    requests = ServiceRequest.objects.filter(status='completed')
    return render(request, 'adminmanager/servicerequests/completed.html', {'requests': requests})

def denied_requests(request):
    requests = ServiceRequest.objects.filter(status='denied')
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

# Open
def concierge_open_requests(request):
    requests = ConciergeServiceRequest.objects.filter(status='open')
    return render(request, 'adminmanager/conciergerequests/open.html', {'requests': requests})

# Completed
def concierge_completed_requests(request):
    requests = ConciergeServiceRequest.objects.filter(status='completed')
    return render(request, 'adminmanager/conciergerequests/completed.html', {'requests': requests})

# Denied
def concierge_denied_requests(request):
   
    requests = ConciergeServiceRequest.objects.filter(status='denied')
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].label_from_instance = lambda obj: f"{obj.last_name}, {obj.first_name}"
        self.fields['property'].label_from_instance = lambda obj: obj.address  # Only show address

def walkthrough_report_view(request):
    if request.method == 'POST':
        form = WalkthroughReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminmanager:walkthrough-success')
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

# Create View
def clientmanager_create_view(request):
    if request.method == 'POST':
        data = request.POST
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
        cm.set_password(data.get('password'))
        cm.save()
        messages.success(request, "Client Manager created successfully.")
        return redirect('adminmanager:list')
    return render(request, 'adminmanager/clientmanager/clientmanager_form.html', {
        'action': 'Create',
        'contact_choices': ClientManagers.PREFERRED_CONTACT_CHOICES,
    })

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
        cm.office_phone=data.get('office_phone'),

        cm.preferred_contact_method = data.get('preferred_contact_method')
        if data.get('password'):
            cm.set_password(data.get('password'))
        cm.save()
        messages.success(request, "Client Manager updated successfully.")
        return redirect('adminmanager:list')
    return render(request, 'adminmanager/clientmanager/clientmanager_form.html', {
        'clientmanager': cm,
        'action': 'Edit',
        'contact_choices': ClientManagers.PREFERRED_CONTACT_CHOICES,
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
