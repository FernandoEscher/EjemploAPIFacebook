from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^EjemploAPIFacebook/', include('EjemploAPIFacebook.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$', 'fbapp.views.authorize_app'),
    (r'^set-facebook-info/', 'fbapp.views.set_facebook_info'),
    (r'^profile/(?P<uid>[0-9]+)', 'fbapp.views.show_facebook_profile'),
    (r'^set-status/(?P<uid>[0-9]+)', 'fbapp.views.set_status'),
)

if settings.DEBUG:
        urlpatterns += patterns('',
                (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
        )
 
