from django.contrib import admin
from django.utils.html import format_html
from .models import PropertyManagement
from django.utils.html import format_html

@admin.register(PropertyManagement)
class PropertyManagementAdmin(admin.ModelAdmin):
    list_display = ("address", "client", "client_manager", "created_at", "property_image_preview")
    ordering = ("-created_at",)
    search_fields = ("address", "client__username", "client_manager__username")

    fieldsets = (
        ("Property Details", {
            "fields": ("client", "client_manager", "address","city","state", "street_line1","street_line2", "size_of_home", "number_of_stories", "construction_type", "year_built", "property_pic"),
        }),
        ("Features", {
            "fields": ("has_pool", "gated_community", "impact_windows", "has_hoa", "gated_property", "basketball_court", "tennis_court", "pickleball_court", "hot_tub", "outdoor_kitchen_gazebo", "waterfront"),
        }),
        ("Contact Preferences", {
            "fields": ("preferred_contact_method",),
        }),
    )

    # Method to show image preview
    def property_image_preview(self, obj):
        if obj.property_pic:
            return format_html('<img src="{}" width="100" style="border-radius: 5px;" />', obj.property_pic.url)
        return "-"
    property_image_preview.short_description = "Property Image"


from django.contrib import admin
from .models import PropertyImprovement

@admin.register(PropertyImprovement)
class PropertyImprovementAdmin(admin.ModelAdmin):
    list_display = ('pino', 'client', 'status', 'cost', 'client_approval', 'created_at')
    list_filter = ('status', 'client_approval', 'created_at')
    search_fields = ('pino', 'client__name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

from .models import Floor ,Room

admin.site.register(Floor)
admin.site.register(Room)