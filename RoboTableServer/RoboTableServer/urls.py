from django.conf.urls import patterns, include, url
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'RoboTableServer.views.index', name='index'),
    url(r'^connect/$', 'RoboTableServer.views.connect', name='connect'),
    url(r'^disconnect/$', 'RoboTableServer.views.disconnect', name='disconnect'),
    url(r'^irs/$', 'RoboTableServer.views.get_irs', name='irs'),
    url(r'^irs/(\d+)/$', 'RoboTableServer.views.get_ir'),
    # url(r'^RoboTableServer/', include('RoboTableServer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
