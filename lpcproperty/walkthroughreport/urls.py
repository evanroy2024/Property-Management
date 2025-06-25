# urls.py

from django.urls import path
from .views import my_reports_view ,export_pdf
from . import views
app_name = 'walkthroughreport'

urlpatterns = [
    path('my-reports/', my_reports_view, name='my_reports'),
    path('export_pdf/<int:report_id>/', export_pdf, name='export_pdf'),
    path('export/excel/<int:report_id>/', views.export_excel, name='export_excel'),
    path('export/csv/<int:report_id>/', views.export_csv, name='export_csv'),

    path('open_export_pdf/<int:report_id>/', views.open_export_pdf, name='open_export_pdf'),

    path('reports/', views.all_reports_view, name='all_reports'),
    path('reports/<int:pk>/', views.report_detail_view, name='report_detail'),
    path('reports_open/<int:pk>/', views.report_open_detail_view, name='report_open_detail'),
    path('reports/completed/', views.completed_reports_view, name='completed_reports'),
    path('reports/denied/', views.denied_reports_view, name='denied_reports'),
    path('reports/open/', views.open_reports_view, name='open_reports'),

    path('walkthrough/update/<int:report_id>/', views.update_walkthrough_report, name='update_walkthrough_report'),

    # cost status etc updates 
    path('update-cost/<int:report_id>/', views.update_cost_ajax, name='update-cost-ajax'),
    path('update-approval/<int:report_id>/', views.update_client_approval, name='update-client-approval'),
    path('update-status/<int:report_id>/', views.update_status, name='update-status'),


]


# urlpatterns = [
#     path('my-reports/', my_reports_view, name='my_reports'),
#     # path('export/pdf/<int:report_id>/', views.export_pdf, name='export_pdf'),
#     path('export_pdf/<int:report_id>/', export_pdf, name='export_pdf'),
#     path('export/excel/<int:report_id>/', views.export_excel, name='export_excel'),
#     path('export/csv/<int:report_id>/', views.export_csv, name='export_csv'),
# ]