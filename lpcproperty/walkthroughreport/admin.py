
# from django.contrib import admin
# from .models import InspectionReport

# @admin.register(InspectionReport)
# class InspectionReportAdmin(admin.ModelAdmin):
#     readonly_fields = ('created_at',)

#     fieldsets = (
#         ('Inspector Info', {
#             'fields': ('inspector_name', 'created_at')
#         }),

#         ('Kitchen Inspection', {
#             'fields': (
#                 'kitchen_counter_clean', 'kitchen_counter_clean_remarks',
#                 'kitchen_appliances_working', 'kitchen_appliances_working_remarks',
#                 'kitchen_floor_clean', 'kitchen_floor_clean_remarks',
#             )
#         }),

#         ('Bedroom Inspection', {
#             'fields': (
#                 'bedroom_bed_made', 'bedroom_bed_made_remarks',
#                 'bedroom_lights_functional', 'bedroom_lights_functional_remarks',
#                 'bedroom_clean_floor', 'bedroom_clean_floor_remarks',
#             )
#         }),

#         ('Bathroom Inspection', {
#             'fields': (
#                 'bathroom_sink_clean', 'bathroom_sink_clean_remarks',
#                 'bathroom_toilet_sanitized', 'bathroom_toilet_sanitized_remarks',
#                 'bathroom_floor_dry', 'bathroom_floor_dry_remarks',
#             )
#         }),
#     )



from django.contrib import admin
from django import forms
from .models import WalkthroughReport, MCQ_CHOICES

class WalkthroughReportForm(forms.ModelForm):
    class Meta:
        model = WalkthroughReport
        fields = '__all__'
        widgets = {
            f'gie{i}': forms.RadioSelect(choices=MCQ_CHOICES)
            for i in range(1, 16)
        }

@admin.register(WalkthroughReport)
class WalkthroughReportAdmin(admin.ModelAdmin):
    form = WalkthroughReportForm

    fieldsets = (
        ('Client Info', {
            'fields': ('user','name', 'description','cost','status','updatedate')
        }),
        ('General Items - Interior', {
            'fields': [
                (f'gie{i}', f'gie{i}_remarks') for i in range(1, 16)
            ]
        }),
        ('General Items - Exterior', {
            'fields': [
                (f'gii{i}', f'gii{i}_remarks') for i in range(1, 10)  # Fixed this part
            ]
        }),
    )
