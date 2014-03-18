from django.conf import settings
from django.conf.urls import patterns, url


urlpatterns = patterns(

    # since this is a single app project, everything can just route to the shipping views
    'apps.shipping.views',

    url(r'^optimize_shipping/', 'optimize'),
    url(r'^', 'home'),
)

if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
