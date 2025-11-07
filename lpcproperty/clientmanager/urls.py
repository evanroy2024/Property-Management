# urls.py
from django.urls import path
from . import views
from .views import client_manager_login_view

app_name = 'clientmanager'


urlpatterns = [
    path('', client_manager_login_view, name='client_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path("profile/update/", views.cm_profile_update, name="cm_profile_update"),
    # property 
    path('properties/', views.property_list_view, name='property_list'),
    path('properties/create/', views.property_create_view, name='property_create'),
    path('properties/<int:pk>/', views.property_detail_view, name='property_detail'),
    path('properties/<int:pk>/edit/', views.property_update_view, name='property_edit'),
    path('properties/<int:pk>/delete/', views.property_delete_view, name='property_delete'),
    path('property/<int:pk>/export/', views.export_property_pdf, name='export_property_pdf'),   # Export Feature

    # Vendors 
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/create/', views.create_vendor, name='create_vendor'),
    path('vendors/<int:vendor_id>/edit/', views.edit_vendor, name='edit_vendor'),
    path('vendors/<int:vendor_id>/delete/', views.delete_vendor, name='delete_vendor'),
    path('vendors/services/', views.manage_vendor_services, name='manage_vendor_services'),
    path('vendor/<int:vendor_id>/details/', views.vendor_details, name='vendor_details'),

    # services completed , pending , denied , opened 
    path('service-requests/pending/', views.pending_requests, name='clientmanager_pending_requests'),
    path('service-requests/open/', views.open_requests, name='clientmanager_open_requests'),
    path('service-requests/completed/', views.completed_requests, name='clientmanager_completed_requests'),
    path('service-requests/denied/', views.denied_requests, name='clientmanager_denied_requests'),
    path('service-requests/<int:request_id>/update/', views.update_service_request, name='clientmanager_update_request'),
    path('service-request/<int:request_id>/view/', views.service_request_detail, name='clientmanager_view_request'),
    path('update-service-cost/', views.update_service_cost, name='update_service_cost'),    # new 
    path('modify-client-approval/', views.modify_client_approval, name='modify_client_approval'),  # new 
    path('change-request-status/', views.change_request_status, name='change_request_status'),  # new 

    # Concierge Service Request URLs                            ( Frontend Done )
    path('concierge/pending/', views.concierge_pending_requests, name='concierge_pending_requests'),
    path('concierge/open/', views.concierge_open_requests, name='concierge_open_requests'),
    path('concierge/completed/', views.concierge_completed_requests, name='concierge_completed_requests'),
    path('concierge/denied/', views.concierge_denied_requests, name='concierge_denied_requests'),
    path('concierge/update/<int:request_id>/', views.update_concierge_request, name='concierge_update_request'),
    path('concierge/view/<int:request_id>/', views.view_concierge_request, name='concierge_view_request'),
    path('update-concierge-cost/', views.update_concierge_cost, name='update_concierge_cost'),  # new 
    path('modify-concierge-approval/', views.modify_concierge_approval, name='modify_concierge_approval'), # new 
    path('change-concierge-status/', views.change_concierge_status, name='change_concierge_status'), # new 

    # Pre Arrival Request To Client 
    path('prearrival/requests/', views.clientmanager_prearrival_requests, name='prearrival_requests'),
    path('prearrival/requests/<int:request_id>/', views.clientmanager_prearrival_detail, name='prearrival_request_detail'),
    path('prearrival/requests/completed/', views.clientmanager_prearrival_completed_requests, name='prearrival_completed_requests'),
    path('update-prearrival-cost/', views.upodate_prearrival_cost, name='upodate_prearrival_cost'),
    path('update-prearrival-approval/', views.upodate_prearrival_approval, name='upodate_prearrival_approval'),
    path('update-prearrival-status/', views.upodate_prearrival_status, name='upodate_prearrival_status'),

    # Depeartaure Information 
    path('departure/requests/', views.clientmanager_departure_requests, name='departure_requests'),
    path('departure/completed/', views.clientmanager_departure_completed_requests, name='departure_completed'),
    path('update-departure-cost/', views.upodate_departure_cost, name='upodate_departure_cost'),
    path('update-departure-approval/', views.upodate_departure_approval, name='upodate_departure_approval'),
    path('update-departure-status/', views.upodate_departure_status, name='upodate_departure_status'),
    path('departure/requests/<int:request_id>/', views.clientmanager_departure_detail, name='departure_request_detail'),


    # walkthroughreport URLS 
    path('reports/', views.all_reports_view, name='all_reports'),
    path('reports/<int:pk>/', views.report_detail_view, name='report_detail'),
    path('reports_open/<int:pk>/', views.report_open_detail_view, name='report_open_detail'),
    path('reports/completed/', views.completed_reports_view, name='completed_reports'),
    path('reports/denied/', views.denied_reports_view, name='denied_reports'),
    path('reports/open/', views.open_reports_view, name='open_reports'),

]
