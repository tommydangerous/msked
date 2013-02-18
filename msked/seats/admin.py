from django.contrib import admin
from seats.models import Seat

class SeatAdmin(admin.ModelAdmin):
    list_display  = ['created', 'station', 'name']
    list_filter   = ['station']
    search_fields = ['name', 'station']

admin.site.register(Seat, SeatAdmin)