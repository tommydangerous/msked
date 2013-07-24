from django.contrib import admin
from teams.models import Team

class TeamAdmin(admin.ModelAdmin):
    fields        = ('name', 'location')
    list_display  = ('pk', 'name', 'employees_count', 'employees', 'location',)
    list_display_links = ('pk', 'name',)
    search_fields = ('name',)

admin.site.register(Team, TeamAdmin)