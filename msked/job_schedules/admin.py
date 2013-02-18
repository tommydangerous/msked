from django.contrib import admin
from job_schedules.models import JobSchedule

class JobScheduleAdmin(admin.ModelAdmin):
    list_display  = ('created', 'schedule', 'job')
    list_filter   = ('schedule',)
    search_fields = ('job', 'schedule')

admin.site.register(JobSchedule, JobScheduleAdmin)