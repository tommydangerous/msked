from django.conf.urls import patterns, url

urlpatterns = patterns('schedules.views',
    url(r'^(?P<pk>[\d]+)/$', 'detail'),
    url(r'^(?P<pk>[\d]+)/assignment/$', 'assignment'),
    url(r'^(?P<pk>[\d]+)/jobs/$', 'jobs'),
    url(r'^(?P<pk>[\d]+)/locations/$', 'locations'),
    url(r'^(?P<pk>[\d]+)/placement/$', 'placement'),
    url(r'^(?P<pk>[\d]+)/task/$', 'task'),
)