from django.contrib import admin
from job_schedules.models import JobSchedule
from location_schedules.models import LocationSchedule
from schedules.models import Schedule

class JobScheduleInline(admin.TabularInline):
    model = JobSchedule
    extra = 1

class LocationScheduleInline(admin.TabularInline):
    model = LocationSchedule
    extra = 1

class ScheduleAdmin(admin.ModelAdmin):
    inlines = [JobScheduleInline, LocationScheduleInline]
    list_filter   = ('created', 'name', 'user')
    search_fields = ('name',)

admin.site.register(Schedule, ScheduleAdmin)