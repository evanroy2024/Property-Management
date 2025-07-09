from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PrearrivalInformation
from mainapp.models import Client


def service_request(request):
    return render(request, "services/service_request.html")

def prearrival_form_view(request):
    # Check if the user is authenticated as a Client
    client_id = request.session.get("client_id")  # Assuming you store client ID in session
    if not client_id:
        messages.error(request, "You must be logged in to submit this form.")
        return redirect("mainapp:client_login")  # Redirect to login page

    try:
        client = Client.objects.get(id=client_id)  # Get the Client instance
    except Client.DoesNotExist:
        messages.error(request, "Invalid user session.")
        return redirect("mainapp:client_login")

    if request.method == "POST":
        name = request.POST.get("name")
        arrival_date = request.POST.get("arrival_date")
        arrival_time = request.POST.get("arrival_time")

        # Validate required fields
        if not name or not arrival_date or not arrival_time:
            messages.error(request, "Name, Arrival Date, and Arrival Time are required.")
            return redirect("servicesapp:prearrival_form")

        # Create PrearrivalInformation entry
        prearrival_info = PrearrivalInformation.objects.create(
            user=client,  # Assign Client instance
            name=name,
            arrival_date=arrival_date,
            arrival_time=arrival_time,
            temperature=request.POST.get("temperature") or None,
            pool_temperature=request.POST.get("pool_temperature") or None,
            hot_bath_temperature=request.POST.get("hot_bath_temperature") or None,
            indoor_lights=request.POST.get("indoor_lights") or None,
            outdoor_lights=request.POST.get("outdoor_lights") or None,
            window_position=request.POST.get("window_position") or None,
            music_genre=request.POST.get("music_genre") or None,
            flower_type=request.POST.get("flower_type") or None,
            flower_location=request.POST.get("flower_location") or None,
            groceries_details=request.POST.get("groceries_details") or None,
            alcohol=request.POST.get("alcohol") or None,
            housekeeping=request.POST.get("housekeeping") or None,
            transportation=request.POST.get("transportation") or None,
            automobiles=request.POST.get("automobiles") or None,
            additional=request.POST.get("additional") or None,
        )
        # messages.success(request, "Prearrival information submitted successfully!")
        return redirect("servicesapp:request_form_success")

    return render(request, "services/prearrival_form.html",{"client": client})

def prearrival_form_success(request):
    messages.success(request, "Your request has been submitted successfully!")
    return render(request, "services/prearrival-success.html")

from django.shortcuts import render, redirect
from .models import DepartureInformation, Client  

def departure_form_view(request):
    client_id = request.session.get("client_id")  # Assuming you store client ID in session
    if not client_id:
        messages.error(request, "You must be logged in to submit this form.")
        return redirect("mainapp:client_login")  # Redirect to login page

    try:
        client = Client.objects.get(id=client_id)  # Get the Client instance
    except Client.DoesNotExist:
        messages.error(request, "Invalid user session.")
        return redirect("mainapp:client_login")
    if request.method == "POST":
        name = request.POST.get("name")
        departure_date = request.POST.get("departure_date")
        departure_time = request.POST.get("departure_time")

        # Ensure mandatory fields are provided
        if not name or not departure_date or not departure_time:
            return render(request, "services/departure_form.html", {"error": "Name, Date, and Time are required!"})

        # Optional fields (set to None if empty)
        housekeeping = request.POST.get("housekeeping") or None
        wash = request.POST.get("wash") or None
        trash = request.POST.get("trash") or None
        additional = request.POST.get("additional") or None

        # Retrieve the client instance from session (Assuming session stores client ID)
        client_instance = Client.objects.filter(id=request.session.get("client_id")).first()

        if client_instance:  
            DepartureInformation.objects.create(
                user=client_instance,
                name=name,
                departure_date=departure_date,
                departure_time=departure_time,
                housekeeping=housekeeping,
                wash=wash,
                trash=trash,
                additional=additional,
            )
            return redirect("servicesapp:request_form_success")  # Redirect to success page

    return render(request, "services/departure_form.html" ,{"client": client})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ConciergeServiceRequest
from mainapp.models import Client, Vendor  # Import Client and Vendor from mainapp

def Concierge_request(request):
    # Check if the user is authenticated as a Client
    client_id = request.session.get("client_id")  # Assuming client ID is stored in session
    if not client_id:
        messages.error(request, "You must be logged in to submit this form.")
        return redirect("mainapp:client_login")  # Redirect to login page

    try:
        client = Client.objects.get(id=client_id)  # Get the Client instance
    except Client.DoesNotExist:
        messages.error(request, "Invalid user session.")
        return redirect("mainapp:client_login")  # Redirect to login page

    if request.method == "POST":
        description = request.POST.get("description")

        ConciergeServiceRequest.objects.create(
            user=client,  # Use Client instance as the user
            description=description
        )

        # messages.success(request, "Your request has been submitted successfully!")
        return redirect("servicesapp:request_form_success")
    return render(request, "services/concierge_request.html")

