from django.conf.urls import patterns, url

urlpatterns = patterns('undos.views', 
    url(r'^$', 'list'),
    url(r'^(?P<pk>\d+)/delete/$', 'delete'),
)