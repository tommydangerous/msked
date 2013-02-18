from assignments.models import Assignment
from django.contrib import admin

class AssignmentAdmin(admin.ModelAdmin):
    list_display  = ['created', 'seat', 'employee', 'station']
    list_filter   = ['seat']
    search_fields = ['employee', 'seat']

admin.site.register(Assignment, AssignmentAdmin)