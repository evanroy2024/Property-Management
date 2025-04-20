from django.contrib import admin
from .models import ServiceRequest

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'request_type', 'status', 'vendor', 'created_at')
    list_filter = ('status', 'request_type', 'vendor')
    search_fields = ('user__username', 'request_type', 'vendor__company_name')
    ordering = ('-created_at',)
    list_editable = ('status', 'vendor')

    readonly_fields = ('created_at',)  # Make created_at visible

admin.site.register(ServiceRequest, ServiceRequestAdmin)


from django.contrib import admin
from .models import PrearrivalInformation

@admin.register(PrearrivalInformation)
class PrearrivalInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'arrival_date', 'arrival_time', 'temperature', 'pool_temperature', 'hot_bath_temperature')
    list_filter = ('arrival_date', 'indoor_lights', 'outdoor_lights', 'window_position')
    search_fields = ('name', 'user__username', 'music_genre', 'flower_type', 'flower_location')

    fieldsets = (
        ('User Information', {'fields': ('user', 'name', 'status','arrival_date', 'arrival_time')}),
        ('Temperature Settings', {'fields': ('temperature', 'pool_temperature', 'hot_bath_temperature')}),
        ('Lighting & Windows', {'fields': ('indoor_lights', 'outdoor_lights', 'window_position')}),
        ('Preferences', {'fields': ('music_genre', 'flower_type', 'flower_location')}),
        ('Additional Details', {'fields': ('groceries_details', 'alcohol', 'housekeeping', 'transportation', 'automobiles', 'additional')}),
    )

from django.contrib import admin
from .models import DepartureInformation

@admin.register(DepartureInformation)
class DepartureInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'departure_date', 'departure_time')
    search_fields = ('name', 'user__username')
    list_filter = ('departure_date',)

    fieldsets = (
        ('User & Departure Details', {
            'fields': ('user', 'name', 'departure_date', 'departure_time'),
            'classes': ('wide',),
        }),
        ('Services', {
            'fields': ('housekeeping', 'wash', 'trash', 'additional'),
            'classes': ('collapse',),
        }),
    )




from django.contrib import admin
from .models import ConciergeServiceRequest

@admin.register(ConciergeServiceRequest)
class ConciergeServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'vendor', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__name', 'vendor__name', 'description')
    ordering = ('-created_at',)
