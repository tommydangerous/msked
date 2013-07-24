from django.contrib import admin
from seats.models import Seat
from stations.models import Station

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 4

class StationAdmin(admin.ModelAdmin):
    inlines       = [SeatInline]
    list_display  = ('created', 'name', 'location', 'job', 'slug',)
    list_filter   = ['location']
    search_fields = ['name']

admin.site.register(Station, StationAdmin)