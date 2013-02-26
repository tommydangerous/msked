from django.contrib import admin
from teams.models import Team

class TeamAdmin(admin.ModelAdmin):
    fields        = ('name', 'location')
    list_display  = ('name', 'location', 'created')
    search_fields = ('name',)

admin.site.register(Team, TeamAdmin)