from django.contrib import admin
from tasks.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display  = ['created', 'job', 'employee', 'employee_pk']
    list_filter   = ['job', 'employee']
    search_fields = ['employee', 'job']

admin.site.register(Task, TaskAdmin)