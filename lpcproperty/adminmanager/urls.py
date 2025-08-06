from django.urls import path
from . import views

app_name = 'adminmanager'

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),

    # Admin Profile 
    path('admin/profile/', views.admin_profile, name='admin_profile'),
    path('admin/profile/edit/', views.edit_admin_profile, name='edit_admin_profile'),
    path('admin/create/', views.create_admin_user, name='create_admin_user'),

    # For Faq Requirements 
    path('faqs/', views.admin_faq_list, name='admin_faq_list'),
    path('faqs/edit/<int:faq_id>/', views.admin_faq_edit, name='admin_faq_edit'),
    path('faqs/create/', views.admin_faq_create, name='admin_faq_create'),
    path('faqs/delete/<int:faq_id>/', views.admin_faq_delete, name='admin_faq_delete'),

    # Testimonials 
    path('testimonials/', views.admin_testimonial_list, name='testimonial_list'),
    path('testimonials/create/', views.admin_testimonial_create, name='testimonial_create'),
    path('testimonials/edit/<int:testimonial_id>/', views.admin_testimonial_edit, name='testimonial_edit'),
    path('testimonials/delete/<int:testimonial_id>/', views.admin_testimonial_delete, name='testimonial_delete'),

    # Social Configurations 
    # Social Links URLs
    path('social-links/', views.social_links_list, name='social_links_list'),
    path('social-links/create/', views.social_links_create, name='social_links_create'),
    path('social-links/<int:pk>/edit/', views.social_links_edit, name='social_links_edit'),
    path('social-links/<int:pk>/delete/', views.social_links_delete, name='social_links_delete'),


    # Mail Configuration URLs
    path('mail-config/', views.mail_config_list, name='mail_config_list'),
    path('mail-config/create/', views.mail_config_create, name='mail_config_create'),
    path('mail-config/<int:pk>/edit/', views.mail_config_edit, name='mail_config_edit'),
    path('mail-config/<int:pk>/delete/', views.mail_config_delete, name='mail_config_delete'),

    # clients --------------------------------------------------------------------------------------------------------------
    path('clients/all/', views.client_list_page, name='client_list_page'),
    path('clients/edit/<int:client_id>/', views.client_edit_page, name='client_edit_page'),
    path('clients/create/', views.create_new_client_view, name='client_create_view'),

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

    # Client Manager Profile 
    # path('clientmanager/profile/', views.clientmanager_profile_view, name='clientmanager_profile_view'),
    # path('clientmanager/profile/edit/', views.clientmanager_profile_edit, name='clientmanager_profile_edit'),
    path('clientmanager/', views.clientmanager_list_view, name='list'),
    path('clientmanager/<int:pk>/', views.clientmanager_detail_view, name='detail'),
    path('clientmanager/create/', views.clientmanager_create_view, name='create'),
    path('clientmanager/<int:pk>/edit/', views.clientmanager_edit_view, name='edit'),
    path('clientmanager/<int:pk>/delete/', views.clientmanager_delete_view, name='delete'),

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

    # Add these to your urls.py
    path('update-concierge-cost/', views.update_concierge_cost, name='update_concierge_cost'),  # new 
    path('modify-concierge-approval/', views.modify_concierge_approval, name='modify_concierge_approval'), # new 
    path('change-concierge-status/', views.change_concierge_status, name='change_concierge_status'), # new 

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

    path('send-email/', views.send_email_view, name='send_email'),

    path('update-cost/', views.update_cost, name='update_cost'),
    path('update-concierge-cost/', views.update_concierge_cost, name='update_concierge_cost'),

    # For services updates 


]
