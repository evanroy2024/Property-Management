from django.shortcuts import redirect
from functools import wraps

def client_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'client_id' not in request.session:  # Check if client is logged in
            return redirect('mainapp:client_login')  # Redirect to login page if not logged in
        return view_func(request, *args, **kwargs)
    return wrapper
