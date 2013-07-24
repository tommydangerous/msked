from django.contrib import admin
from notes.models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'created', 'user', 'employee', 'station', 'short', 
        'updated')
    list_filter   = ('employee', 'user',)
    search_fields = ('content', 'employee', 'user',)

admin.site.register(Note, NoteAdmin)