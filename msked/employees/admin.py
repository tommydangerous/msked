from django.contrib import admin
from employees.models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'tier_lab', 'tier_office', 'team', 
        'floater', 'vacation', 'image',)
    list_display = ('pk', 'last_name', 'first_name', 'tier_lab', 'tier_office', 
        'admin_team', 'floater', 'vacation', 'current_location', 'image',)
    list_display_links = ('last_name', 'first_name')
    list_filter        = ('team', 'tier_lab', 'tier_office')
    ordering           = ('last_name',)
    search_fields      = ('first_name', 'last_name')

admin.site.register(Employee, EmployeeAdmin)