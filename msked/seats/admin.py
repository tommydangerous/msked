from django.contrib import admin
from seats.models import Seat

class SeatAdmin(admin.ModelAdmin):
    list_display  = ['created', 'station', 'name', 'job']
    list_filter   = ['station', 'job']
    search_fields = ['name', 'station', 'job']

admin.site.register(Seat, SeatAdmin)