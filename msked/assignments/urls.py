from django.conf.urls import patterns, url

urlpatterns = patterns('assignments.views',
    url(r'^(?P<slug>[-\w]+)/new/$', 'new'),
    url(r'^(?P<pk>[-\w]+)/edit/$', 'edit'),
)