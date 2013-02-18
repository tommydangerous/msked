from django.contrib import admin
from django.contrib.auth.models import User
from users.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display  = ('created', 'user', 'login_count', 'slug')
    search_fields = ('user',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'first_name', 'last_name', 'email', 
        'is_staff', 'last_login', 'date_joined')
    list_display_links = ('username',)
    search_fields = ('email', 'first_name', 'last_name', 'username')

admin.site.unregister(User)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UserAdmin)