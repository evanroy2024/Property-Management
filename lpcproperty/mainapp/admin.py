from django.contrib import admin
from .models import Client
from django.contrib import admin
from .models import Client

from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'preferred_contact_method', 'created_at')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('preferred_contact_method', 'created_at')

    fieldsets = (
        ("Personal Information", {
            "fields": ("first_name", "last_name", "username", "email", "password"),
        }),
        ("Address Information", {
            "fields": ("address", "city", "state", "zipcode","phone_number", "preferred_contact_method"),
        }),
        ("Preffered Contact 1", {
            "fields": ("contact1_name", "contact1_email", "contact1_phone", "contact1_preferred"),
        }),
        ("Preffered Contact 2", {
            "fields": ("contact2_name", "contact2_email", "contact2_phone", "contact2_preferred"),
        }),
        ("Preffered Contact 3", {
            "fields": ("contact3_name", "contact3_email", "contact3_phone", "contact3_preferred"),
        }),
    )

admin.site.site_header = "Admin Panel"
admin.site.site_title = "Client Management"
admin.site.index_title = "Manage Clients"

from django.contrib import admin
from .models import ClientManagers

@admin.register(ClientManagers)
class ClientManagersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'city', 'preferred_contact_method', 'created_at')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('city', 'preferred_contact_method', 'created_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username', 'email', 'password', 'phone_number')}),
        ('Address', {'fields': ('city', 'state', 'zipcode')}),
        ('Preferences', {'fields': ('preferred_contact_method',)}),
    )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])  # Hash password before saving
        super().save_model(request, obj, form, change)




from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("company_name", "username", "email", "phone_number", "city", "state", "service")
    search_fields = ("company_name", "username", "email", "phone_number", "city")
    list_filter = ("state", "service")
    ordering = ("company_name",)
