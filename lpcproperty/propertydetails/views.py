from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import Client
from .models import PropertyImprovement

def generate_pino(client):
    """Generates a unique PINO based on the client's username."""
    username = client.username.upper()  # Convert username to uppercase
    count = PropertyImprovement.objects.filter(client=client).count() + 1  # Increment count
    return f"{username}_PI_{count:03d}"  # Format as USERNAME_PI_001

def property_improvements(request):
    # Check if the user is authenticated as a Client
    client_id = request.session.get("client_id")
    if not client_id:
        messages.error(request, "You must be logged in to submit this form.")
        return redirect("mainapp:client_login")

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        messages.error(request, "Invalid user session.")
        return redirect("mainapp:client_login")

    if request.method == "POST":
        description = request.POST.get("description", "")

        # Auto-generate pino
        pino = generate_pino(client)

        # Create a new property improvement request
        PropertyImprovement.objects.create(
            client=client,
            pino=pino,
            description=description
        )

        messages.success(request, "Your property improvement request has been submitted!")
        return redirect("propertydetails:property_improvements")  # Redirect to the same page

    return render(request, "property/property_improvement.html")






from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PropertyImprovement

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PropertyImprovement

def open_property_improvements(request):
    client_id = request.session.get("client_id")

    if not client_id:
        messages.error(request, "You must be logged in to view this page.")
        return redirect("mainapp:client_login")

    property_improvements = PropertyImprovement.objects.filter(client_id=client_id, status="open")

    print(f"Client ID: {client_id}")  # Debugging: Check if client_id exists
    print(f"Query Result: {property_improvements}")  # Debugging: Check what the query returns

    return render(request, "property/open_property_improvements.html", {"property_improvements": property_improvements})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def update_client_approval(request, improvement_id, decision):
    """Allows the logged-in client to approve or deny their property improvement."""
    client_id = request.session.get("client_id")

    if not client_id:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect("mainapp:client_login")

    improvement = get_object_or_404(PropertyImprovement, id=improvement_id, client_id=client_id)

    if decision == "approve":
        improvement.client_approval = "Approved"
    elif decision == "deny":
        improvement.client_approval = "Deny"
    else:
        messages.error(request, "Invalid action.")
        return redirect("propertydetails:open_property_improvements")

    improvement.save()
    messages.success(request, f"Property Improvement {improvement.pino} has been {improvement.client_approval}.")
    return redirect("propertydetails:open_property_improvements")


def completed_property_improvements(request):
    """View to show only completed property improvements for the logged-in client."""
    client_id = request.session.get("client_id")

    if not client_id:
        messages.error(request, "You must be logged in to view this page.")
        return redirect("mainapp:client_login")

    # Fetch only completed improvements
    property_improvements = PropertyImprovement.objects.filter(client_id=client_id, status="completed")

    return render(request, "property/completed_property_improvements.html", {"property_improvements": property_improvements})
