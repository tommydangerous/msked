from django.contrib import admin
from works.models import Work

class WorkAdmin(admin.ModelAdmin):
    list_display  = ['created', 'job', 'employee']
    list_filter   = ['job']
    search_fields = ['employee', 'job']

admin.site.register(Work, WorkAdmin)