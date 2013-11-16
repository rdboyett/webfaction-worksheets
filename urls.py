import os
from  django.conf.urls import *
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.views.static import * 
from django.conf import settings
from django.views.generic import RedirectView
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()


urlpatterns = patterns('',
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
    # Examples:
    #url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^myproject/', include('myproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
)


urlpatterns += patterns('myproject.googleapi.views',
    (r'^$', 'testLoad'),
    (r'^oauth2callback/$', 'auth_return'),
    (r'^login/$', 'index'),
    (r'^drive/$', 'driveUpload'),
    (r'^userInfo/$', 'getUserInfo'),
    (r'^list/$', 'driveList'),
    (r'^create/$', 'startCreate'),
    (r'^getFile/$', 'getFile'),
    (r'^showFile/(?P<fileId>.+)/$', 'showFile'),
    (r'^showFile/$', RedirectView.as_view(url='/getFile/')),
    (r'^convert/$', 'imageConvert'),
    (r'^count/$', 'countPages'),
    (r'^zip/$', 'zipFile'),
    (r'^makeJson/$', 'makeJsonFile'),
    (r'^readJson/$', 'readJsonFile'),
    (r'^test/$', 'updateCorrectAnswer'),
    (r'^nextPage/(?P<projectID>(\d+))/(?P<pageNumber>(\d+))/(?P<totalPages>(\d+))/$', 'showNextPage'),
)


urlpatterns += staticfiles_urlpatterns()