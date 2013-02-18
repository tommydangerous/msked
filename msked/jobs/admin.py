from django.contrib import admin
from excludes.models import Exclude
from jobs.models import Job

class ExcludeInline(admin.TabularInline):
    model = Exclude
    extra = 1

class JobAdmin(admin.ModelAdmin):
    inlines = [ExcludeInline]
    list_display = ['pk', 'name', 'daily', 'weekly', 'team']
    search_fields = ['name']

admin.site.register(Job, JobAdmin)