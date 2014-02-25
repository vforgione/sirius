from django.conf.urls import patterns, url


urlpatterns = patterns(

    # since this is a single app project, everything can just route to the shipping views
    'apps.shipping.views',

    url(r'^optimize_shipping/', 'optimize'),
    url(r'^', 'home'),
)
