from django.contrib import admin
from employees.models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'last_name', 'first_name', 'tier_lab', 
        'tier_office', 'admin_team', 'floater', 'vacation', 'slug']
    list_display_link = ('last_name',)
    list_filter = ['team', 'tier_lab', 'tier_office']
    search_fields = ['first_name', 'last_name']

admin.site.register(Employee, EmployeeAdmin)