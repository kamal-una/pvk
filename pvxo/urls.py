from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'ticketing.views',
    # Examples:
    # url(r'^$', 'pvxo.views.home', name='home'),
    # url(r'^pvxo/', include('pvxo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # generic urls
    url(r'^$', 'home', name='home'),
    url(r'^register/', 'register', name='register'),
    url(r'^myaccount/', 'my_account', name='my_account'),
    url(r'^logout/$', 'user_logout', name='logout'),
)

urlpatterns += patterns(
    'frontend.views',
    url(r'^schedule/$', 'schedule', name='schedule'),
    url(r'^buy/(?P<event>[-\w\ ]+)/$', 'buy', name='buy'),
)

urlpatterns += patterns(
    'django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'login.html'}, name='login'),
)
