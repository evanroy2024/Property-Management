from django.urls import path
from . import views

urlpatterns = [
    path('property/<int:property_id>/messages/', views.view_messages, name='view_messages'),
    path('property/<int:property_id>/send-message/', views.send_message, name='send_message'),
    path('my-properties/', views.my_properties, name='my_properties'),

]
