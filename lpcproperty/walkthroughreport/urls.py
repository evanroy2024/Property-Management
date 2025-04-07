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

    path('reports/', views.all_reports_view, name='all_reports'),
    path('reports/<int:pk>/', views.report_detail_view, name='report_detail'),
    path('reports/completed/', views.completed_reports_view, name='completed_reports'),
    path('reports/denied/', views.denied_reports_view, name='denied_reports'),
    path('reports/open/', views.open_reports_view, name='open_reports'),

]


# urlpatterns = [
#     path('my-reports/', my_reports_view, name='my_reports'),
#     # path('export/pdf/<int:report_id>/', views.export_pdf, name='export_pdf'),
#     path('export_pdf/<int:report_id>/', export_pdf, name='export_pdf'),
#     path('export/excel/<int:report_id>/', views.export_excel, name='export_excel'),
#     path('export/csv/<int:report_id>/', views.export_csv, name='export_csv'),
# ]