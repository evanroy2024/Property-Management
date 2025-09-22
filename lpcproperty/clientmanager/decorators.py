# decorators.py
from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from mainapp.models import ClientManagers

def client_manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if manager_id exists in session
        manager_id = request.session.get('manager_id')
        if not manager_id:
            return HttpResponseForbidden("Login required")
        
        # Get the logged-in client manager from session
        try:
            logged_in_cm = ClientManagers.objects.get(id=manager_id)
            request.client_manager = logged_in_cm
        except ClientManagers.DoesNotExist:
            return HttpResponseForbidden("Invalid client manager")
        
        return view_func(request, *args, **kwargs)
    return wrapper
