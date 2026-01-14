from django.urls import path
from .views import prearrival_form_view , departure_form_view , service_request,Concierge_request , prearrival_form_success , concierge_form_success
from . import views
app_name = 'servicesapp'

urlpatterns = [
    path("prearrival/", prearrival_form_view, name="prearrival_form"),
    path("departure/", departure_form_view, name="departure_form"),
    path("service_request/", service_request, name="service_request"),

    path("concierge_request/", Concierge_request, name="Concierge_request"),

    path("request-success/", views.service_form_success, name="request_form_success"),

    path("concierge-success/", views.concierge_form_success, name="concierge_form_success"),

    path("prearrival-success/", views.prearrival_form_success, name="prearrival_form_success"),

    path("departure-success/", views.departure_form_success, name="departure_form_success"),


    
]