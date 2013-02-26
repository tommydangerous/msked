from django.contrib import admin
from placements.models import Placement

class PlacementAdmin(admin.ModelAdmin):
    list_display  = ('created', 'admin_location', 'admin_employee', 'team')
    list_filter   = ('location', 'employee')
    search_fields = ('employee', 'location')

admin.site.register(Placement, PlacementAdmin)