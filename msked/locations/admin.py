from django.contrib import admin
from locations.models import Location

class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'occupancy', 'slug']
    search_fields = ['name']

admin.site.register(Location, LocationAdmin)