from django.urls import path
from .views import property_improvements
from .views import open_property_improvements, update_client_approval , completed_property_improvements

app_name = 'propertydetails'

urlpatterns = [
    path('property_improvement/', property_improvements, name='property_improvements'),
    path('property-improvements/open/', open_property_improvements, name='open_property_improvements'),
    path('property-improvements/update/<int:improvement_id>/<str:decision>/', update_client_approval, name='update_client_approval'),
    path('property-improvements/completed/', completed_property_improvements, name='completed_property_improvements'),
]
