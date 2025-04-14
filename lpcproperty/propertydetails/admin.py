from django.contrib import admin
from django.utils.html import format_html
from .models import PropertyManagement

@admin.register(PropertyManagement)
class PropertyManagementAdmin(admin.ModelAdmin):
    list_display = ("address", "client", "client_manager", "created_at")  # ✅ Ensure created_at exists in the model
    ordering = ("-created_at",)  # ✅ Fix ordering by making sure created_at exists
    search_fields = ("address", "client__username", "client_manager__username")

    fieldsets = (
        ("Property Details", {
            "fields": ("client", "client_manager", "address", "size_of_home", "number_of_stories", "construction_type", "year_built"),
        }),
        ("Features", {
            "fields": ("has_pool", "gated_community", "impact_windows", "has_hoa", "gated_property"),
        }),
        ("Contact Preferences", {
            "fields": ("preferred_contact_method",),
        }),
       
    )

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