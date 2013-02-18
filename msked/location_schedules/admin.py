from django.contrib import admin
from location_schedules.models import LocationSchedule

class LocationScheduleAdmin(admin.ModelAdmin):
    list_display  = ('created', 'schedule', 'location')
    list_filter   = ('schedule',)
    search_fields = ('location', 'schedule')

admin.site.register(LocationSchedule, LocationScheduleAdmin)