from django.conf.urls import patterns, url

urlpatterns = patterns('employees.views', 
    url(r'^$', 'list'),
    url(r'^new/$', 'new'),
    url(r'^(?P<slug>[-\w]+)/$', 'detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'edit'),
    url(r'^(?P<slug>[-\w]+)/(?P<item>jobs|locations|seats)/$', 'history'),
    url(r'^(?P<slug>[-\w]+)/notes/$', 'notes'),
)