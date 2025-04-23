from django.urls import path
from .views import prearrival_form_view , departure_form_view , service_request,Concierge_request , prearrival_form_success

app_name = 'servicesapp'

urlpatterns = [
    path("prearrival/", prearrival_form_view, name="prearrival_form"),
    path("departure/", departure_form_view, name="departure_form"),
    path("service_request/", service_request, name="service_request"),

    path("Concierge_request/", Concierge_request, name="Concierge_request"),

    path("request-success/", prearrival_form_success, name="request_form_success"),
    
]