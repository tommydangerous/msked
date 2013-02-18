from django.conf.urls import patterns, url

urlpatterns = patterns('placements.views',
    url(r'^(?P<slug>[-\w]+)/new/$', 'new'),
    url(r'^(?P<pk>[\d]+)/edit/$', 'edit'),
    url(r'^delete-all/$', 'delete_all'),
)