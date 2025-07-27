from django.contrib import admin
from .models import (
    WalkthroughReport, GeneralItemsExterior, GeneralItemsInterior,
    Garage, Laundry, Kitchen, Butlers, BreakfastArea, EntryFoyer,
    GreatRoom, DiningRoom, ClosetsMainLevel, ClosetsUpperLevel,
    HallwaysMainLevel, HallwaysUpperLevel, Bedroom1, Bedroom2,
    Bedroom3, Bedroom4, Bedroom5, Bedroom6, Bedroom7, Bedroom8,
    Bedroom9, Bedroom10, Bathroom1, Bathroom2, Bathroom3, Bathroom4,
    Bathroom5, Bathroom6, Bathroom7, Bathroom8, Bathroom9, Bathroom10,
    Bathroom11, Bathroom12, Gym, TheatreMusicRoom, GuestHouseSleepingLiving ,GuestHouseBathroom
)

@admin.register(WalkthroughReport)
class WalkthroughReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'status', 'client_approval', 'datetime']
    list_filter = ['status', 'client_approval', 'datetime']
    search_fields = ['name', 'description', 'user__username']
    list_editable = ['status']

@admin.register(GeneralItemsExterior)
class GeneralItemsExteriorAdmin(admin.ModelAdmin):
    list_display = ['walkthrough_report', 'gie1', 'gie2', 'gie3']

@admin.register(GeneralItemsInterior)
class GeneralItemsInteriorAdmin(admin.ModelAdmin):
    list_display = ['walkthrough_report', 'gii1', 'gii2', 'gii3']

admin.site.register(Garage)
admin.site.register(Laundry)
admin.site.register(Kitchen)
admin.site.register(Butlers)
admin.site.register(BreakfastArea)
admin.site.register(EntryFoyer)
admin.site.register(GreatRoom)
admin.site.register(DiningRoom)
admin.site.register(ClosetsMainLevel)
admin.site.register(ClosetsUpperLevel)
admin.site.register(HallwaysMainLevel)
admin.site.register(HallwaysUpperLevel)
admin.site.register(Bedroom1)
admin.site.register(Bedroom2)
admin.site.register(Bedroom3)
admin.site.register(Bedroom4)
admin.site.register(Bedroom5)
admin.site.register(Bedroom6)
admin.site.register(Bedroom7)
admin.site.register(Bedroom8)
admin.site.register(Bedroom9)
admin.site.register(Bedroom10)
admin.site.register(Bathroom1)
admin.site.register(Bathroom2)
admin.site.register(Bathroom3)
admin.site.register(Bathroom4)
admin.site.register(Bathroom5)
admin.site.register(Bathroom6)
admin.site.register(Bathroom7)
admin.site.register(Bathroom8)
admin.site.register(Bathroom9)
admin.site.register(Bathroom10)
admin.site.register(Bathroom11)
admin.site.register(Bathroom12)
admin.site.register(Gym)
admin.site.register(TheatreMusicRoom)
admin.site.register(GuestHouseSleepingLiving)
admin.site.register(GuestHouseBathroom)