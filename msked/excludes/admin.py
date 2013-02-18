from django.contrib import admin
from excludes.models import Exclude

class ExcludeAdmin(admin.ModelAdmin):
    list_display  = ['created', 'schedule', 'job', 'team']
    list_filter   = ['job', 'team', 'schedule']
    search_fields = ['job', 'team', 'schedule']

admin.site.register(Exclude, ExcludeAdmin)