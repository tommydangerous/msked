from django.conf.urls import patterns, url

urlpatterns = patterns('stations.views',
    url(r'^(?P<slug>[-\w]+)/$', 'detail'),
)