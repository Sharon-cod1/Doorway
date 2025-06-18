from django.contrib import admin

from .models import Property, ContactRequest

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'transaction_type', 'price', 'city', 'is_featured', 'is_published')
    list_filter = ('property_type', 'transaction_type', 'city', 'is_featured', 'is_published')
    search_fields = ('title', 'description', 'location', 'city', 'address')
    prepopulated_fields = {}

admin.site.register(Property, PropertyAdmin)
admin.site.register(ContactRequest)