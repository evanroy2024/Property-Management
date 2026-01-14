
from django.urls import path
from . import views
# from .views import login_view, register_view, otp_verify ,logout_view
# from .views import forgot_password, reset_password , get_started ,
# from .views import testui
from .views import client_login, dashboard, client_logout 
from .views import client_properties , service_request ,pre_arrival , departure , docoments ,  open_services ,completed_services ,denied_services
from .views import completed_concierge_services ,denied_concierge_services , open_concierge_services , client_manager_support 
from .views import manager_login ,manager_home
from .views import home
app_name = 'mainapp'

urlpatterns = [
    path('login/', client_login, name="client_login"),
    path("password/change/", views.ClientPasswordChangeRequestView.as_view(), name="client_password_change"),
    path("password/verify/", views.ClientPasswordVerifyView.as_view(), name="client_password_verify"),
    path('', home, name="home"),
    path('dashboard/', dashboard, name="dashboard"),
    path('docoments/', docoments, name="docoments"),
    path('logout/', client_logout, name="client_logout"),
    path('my-properties/', client_properties, name='client_properties'),
    path('servierequest/', service_request, name='service_request'),  # ✅ Added service request URL

    path("profile/update/", views.client_profile_update, name="client_profile_update"),
    path('learn_more1/', views.learn_more1, name='learn_more1'),  # ✅ Added learn_more1 URL
    path('learn-more2/', views.learn_more2, name='learn_more2'),  # ✅ Added learn_more1 URL
    path('learn-more3/', views.learn_more3, name='learn_more3'),  # ✅ Added learn_more1 URL
    path('get-contact/', views.get_contact, name='get_contact'),  # ✅ Added learn_more1 URL
    path('process/', views.process, name='process'),  # ✅ Added learn_more1 URL
    path('pre_arrival/', pre_arrival, name='pre_arrival'),  # ✅ Added service request URL
    path('departure/', departure, name='departure'),  # ✅ Added service request URL

    path('open_services', open_services, name='open_services'),  # ✅ Added service request URL
    path('completed_services', completed_services, name='completed_services'),  # ✅ Added service request URL
    path('denied_services', denied_services, name='denied_services'),  # ✅ Added service request URL

    path('open_concierge_services', open_concierge_services, name='open_concierge_services'),  # ✅ Added service request URL
    path('completed_concierge_services', completed_concierge_services, name='completed_concierge_services'),  # ✅ Added service request URL
    path('denied_concierge_services', denied_concierge_services, name='denied_concierge_services'),  # ✅ Added service request URL

    path('client_manager_support', client_manager_support, name='client_manager_support'),  # ✅ Added service request URL
    path('manager-login/', manager_login, name='manager_login'),

    path('manager-home/', manager_home, name='manager_home'),  # Ensure this exists



    # WALKTHROUGH REPORT URLS --------------------------------------------------------------------------------------
    path('my-reports/', views.my_reports_view, name='my_reports'),
    path('export_pdf/<int:report_id>/', views.export_pdf, name='export_pdf'),
    path('export/excel/<int:report_id>/', views.export_excel, name='export_excel'),
    path('export/csv/<int:report_id>/', views.export_csv, name='export_csv'),

    path('reports/', views.all_reports_view, name='all_reports'),
    path('reports/<int:pk>/', views.report_detail_view, name='report_detail'),
    path('reports/completed/', views.completed_reports_view, name='completed_reports'),
    path('reports/denied/', views.denied_reports_view, name='denied_reports'),
    path('reports/open/', views.open_reports_view, name='open_reports'),
    path('report/<int:report_id>/status/<str:status>/', views.update_report_status, name='update_report_status'),



    # path('', views.home, name='home'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('login/', login_view, name='login'),
    # path('getstarted/', views.get_started, name='get_started'),  # ✅ Added getstarted URL
    # path('register/', register_view, name='register'),
    # path('otp-verify/', otp_verify, name='otp_verify'),
    # path('logout/', logout_view, name='logout'),  # ✅ Logout URL
    # path("forgot-password/", forgot_password, name="forgot_password"),
    # path("reset-password/<uidb64>/<token>/", reset_password, name="reset_password"),

    # path('testui',testui,name='testui')
    path('privacy/', views.privacy_view, name='privacy'),

    path('update-conformation', views.profile_update , name='profile_conformation_update'),


    # walktrug report url 
    path('walktrug/open/', views.walktrug_open_reports_view, name='item_open_reports'),
    path('walktrug/completed/', views.walktrug_completed_reports_view, name='item_completed_reports'),   
    path('walktrug/denied/', views.walktrug_denied_reports_view, name='item_denied_reports'),   
    path('update-client-approval/<int:report_id>/', views.update_client_approval, name='update-client-approval'),
    

]
