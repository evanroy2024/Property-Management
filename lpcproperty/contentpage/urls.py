from django.urls import path
from . import views

app_name = 'contentpage'

urlpatterns = [
    path('faq/', views.faq, name='faq'),
    path('send-message/', views.send_message_view, name='send_message'),

]
