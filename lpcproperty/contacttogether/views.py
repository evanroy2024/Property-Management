from django.shortcuts import render, get_object_or_404, redirect
from .models import PropertyManagement, Message
from mainapp.models import Client, ClientManagers

from django.shortcuts import render, get_object_or_404, redirect
from .models import Message
from propertydetails.models import PropertyManagement
from mainapp.models import Client, ClientManagers

def view_messages(request, property_id):
    property_obj = get_object_or_404(PropertyManagement, id=property_id)
    messages = Message.objects.filter(property=property_obj).order_by('sent_at')

    return render(request, 'messages/view_messages.html', {
        'property': property_obj,
        'messages': messages
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import PropertyManagement, Message, Client, ClientManagers

def send_message(request, property_id):
    property_obj = get_object_or_404(PropertyManagement, id=property_id)

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()

        if not message_text:
            return redirect('view_messages', property_id=property_id)

        # Clear and precise logic: check manager first
        sender_type = None
        sender_client = None
        sender_manager = None

        if request.session.get('manager_id') and not request.session.get('client_id'):
            sender_type = 'manager'
            sender_manager = ClientManagers.objects.get(id=request.session['manager_id'])

        elif request.session.get('client_id') and not request.session.get('manager_id'):
            sender_type = 'client'
            sender_client = Client.objects.get(id=request.session['client_id'])

        else:
            return redirect('login')  # Invalid state

        # Create the message
        Message.objects.create(
            property=property_obj,
            sender_type=sender_type,
            sender_client=sender_client,
            sender_manager=sender_manager,
            message_text=message_text
        )

        return redirect('view_messages', property_id=property_id)

    return render(request, 'messages/send_message.html', {
        'property': property_obj
    })

def my_properties(request):
    client_id = request.session.get('client_id')
    manager_id = request.session.get('manager_id')

    if client_id:
        properties = PropertyManagement.objects.filter(client_id=client_id)
    elif manager_id:
        properties = PropertyManagement.objects.filter(client_manager_id=manager_id)
    else:
        return redirect('login')

    return render(request, 'messages/client_manager_support.html', {'properties': properties})
