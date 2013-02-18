from django.contrib import admin
from undos.models import Undo

class UndoAdmin(admin.ModelAdmin):
    list_display  = ['created', 'job', 'location']
    list_filter   = ['job', 'location']
    search_fields = ['job', 'location']

admin.site.register(Undo, UndoAdmin)