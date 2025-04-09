from django.contrib import admin
from .models import SocialLinks

@admin.register(SocialLinks)
class SocialLinksAdmin(admin.ModelAdmin):
    list_display = ['id', 'facebook', 'instagram', 'pinterest', 'linkedin']
    search_fields = ['facebook', 'instagram', 'pinterest', 'linkedin']
    
from django.contrib import admin
from .models import MailConfiguration, CallConfiguration

@admin.register(MailConfiguration)
class MailConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'email_host', 'email_port', 'email_host_user', 'use_tls', 'use_ssl')
    search_fields = ('email_host', 'email_host_user')
    list_filter = ('use_tls', 'use_ssl')


@admin.register(CallConfiguration)
class CallConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_provider', 'phone_number', 'use_voice_call', 'use_sms')
    search_fields = ('phone_number', 'service_provider')
    list_filter = ('service_provider', 'use_voice_call', 'use_sms')
