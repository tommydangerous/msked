from django.contrib import admin
from requires.models import Require

class RequireAdmin(admin.ModelAdmin):
    list_display  = ['created', 'job', 'employee']
    list_filter   = ['job']
    search_fields = ['employee', 'job']

admin.site.register(Require, RequireAdmin)