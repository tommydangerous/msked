from django.conf.urls import patterns, url

urlpatterns = patterns('notes.views',
    url(r'^(?P<slug>[-\w]+)/new/$', 'new'),
    url(r'^(?P<pk>[\d]+)/edit/$', 'edit'),
)