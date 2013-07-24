from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': settings.MEDIA_ROOT }),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'sessions.views.new'),
    url(r'^logout/$', 'sessions.views.delete'),
    url(r'^assignments/', include('assignments.urls')),
    url(r'^employees/', include('employees.urls')),
    url(r'^notes/', include('notes.urls')),
    url(r'^placements/', include('placements.urls')),
    url(r'^schedules/', include('schedules.urls')),
    url(r'^stations/', include('stations.urls')),
    url(r'^tasks/', include('tasks.urls')),
    url(r'^undos/', include('undos.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^$', 'schedules.views.root', name='root_path'),
)