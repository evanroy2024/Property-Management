from django.contrib import admin
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    search_fields = ('question', 'answer')
from django.contrib import admin
from .models import Testimonial

admin.site.register(Testimonial)
# admin.py
from django.contrib import admin
from .models import UserMessage

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'need_type')
    search_fields = ('name', 'email', 'need_type')
