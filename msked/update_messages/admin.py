from django.contrib import admin

from update_messages.models import UpdateMessage

class UpdateMessageAdmin(admin.ModelAdmin):
   list_display  = ('pk', 'created', 'content', 'viewed',)
   list_filter   = ('viewed',)
   search_fields = ('content',)

admin.site.register(UpdateMessage, UpdateMessageAdmin)