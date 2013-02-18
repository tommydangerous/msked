from django.contrib import admin
from teams.models import Team

class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    search_fields = ['name']

admin.site.register(Team, TeamAdmin)