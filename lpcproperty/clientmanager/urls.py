# urls.py
from django.urls import path
from . import views

app_name = 'clientmanager'

from .views import client_manager_login_view, client_dashboard_view, client_logout_view

urlpatterns = [
    path('login/', client_manager_login_view, name='client_login'),
    path('dashboard/', client_dashboard_view, name='client_dashboard'),
    path('logout/', client_logout_view, name='client_logout'),

    # clients 
    path('clients/all/', views.client_list_page, name='client_list_page'),
    path('clients/edit/<int:client_id>/', views.client_edit_page, name='client_edit_page'),
    path('clients/create/', views.create_new_client_view, name='client_create_view'),

    # property 
    path('properties/', views.property_list_view, name='property_list'),
    path('properties/create/', views.property_create_view, name='property_create'),
    path('properties/<int:pk>/', views.property_detail_view, name='property_detail'),
    path('properties/<int:pk>/edit/', views.property_update_view, name='property_edit'),
    path('properties/<int:pk>/delete/', views.property_delete_view, name='property_delete'),

    # Vendors 
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/create/', views.create_vendor, name='create_vendor'),
    path('vendors/<int:vendor_id>/edit/', views.edit_vendor, name='edit_vendor'),
    path('vendors/<int:vendor_id>/delete/', views.delete_vendor, name='delete_vendor'),

    # Client Manager Profile 
    path('clientmanager/profile/', views.clientmanager_profile_view, name='clientmanager_profile_view'),
    path('clientmanager/profile/edit/', views.clientmanager_profile_edit, name='clientmanager_profile_edit'),

    # Pre Arrival Request To Client 
    path('prearrival/requests/', views.clientmanager_prearrival_requests, name='prearrival_requests'),
    path('prearrival/requests/<int:request_id>/', views.clientmanager_prearrival_detail, name='prearrival_request_detail'),

    # Depeartaure Information 
    path('departure/requests/', views.clientmanager_departure_requests, name='departure_requests'),
    path('departure/requests/<int:request_id>/', views.clientmanager_departure_detail, name='departure_request_detail'),

    # path('dashboardtrial/', views.client_manager_dashboard, name='client_manager_dashboard'),       #        TO CHECK CM AND CLIENT RELATIUON

    # services completed , pending , denied , opened 
    path('service-requests/pending/', views.pending_requests, name='clientmanager_pending_requests'),
    path('service-requests/open/', views.open_requests, name='clientmanager_open_requests'),
    path('service-requests/completed/', views.completed_requests, name='clientmanager_completed_requests'),
    path('service-requests/denied/', views.denied_requests, name='clientmanager_denied_requests'),
    path('service-requests/<int:request_id>/update/', views.update_service_request, name='clientmanager_update_request'),
    path('service-request/<int:request_id>/view/', views.service_request_detail, name='clientmanager_view_request'),

    # Concierge Service Request URLs                            ( Frontend Done )
    path('concierge/pending/', views.concierge_pending_requests, name='concierge_pending_requests'),
    path('concierge/open/', views.concierge_open_requests, name='concierge_open_requests'),
    path('concierge/completed/', views.concierge_completed_requests, name='concierge_completed_requests'),
    path('concierge/denied/', views.concierge_denied_requests, name='concierge_denied_requests'),
    path('concierge/update/<int:request_id>/', views.update_concierge_request, name='concierge_update_request'),
    path('concierge/view/<int:request_id>/', views.view_concierge_request, name='concierge_view_request'),

    # Property Improvement Details                              ( Frontend Done )
    path('property/pending/', views.property_pending_requests, name='property_pending_requests'),
    path('property/open/', views.property_open_requests, name='property_open_requests'),
    path('property/completed/', views.property_completed_requests, name='property_completed_requests'),
    path('property/denied/', views.property_denied_requests, name='property_denied_requests'),
    path('property/update/<int:request_id>/', views.update_property_request, name='property_update_request'),
    path('property/view/<int:request_id>/', views.view_property_request, name='property_view_request'),

    # Building of walkthrpough report submission 
    # path("walkthrough/submit/", views.submit_walkthrough, name="submit_walkthrough"),
    path('walkthrough/', views.walkthrough_report_view, name='walkthrough-form'),
    path('walkthrough/success/', views.walkthrough_success_view, name='walkthrough-success'),
]
