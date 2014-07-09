from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from boxoffice.views import EventListing, EventCreate, EventUpdate, EventDelete
from boxoffice.views import BuyerListing, BuyerCreate, BuyerUpdate, BuyerDelete
from boxoffice.views import EventCategoryListing, EventCategoryCreate, EventCategoryUpdate, EventCategoryDelete

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
    url(r'^cart/$', 'cart', name='cart'),
    url(r'^empty_cart/$', 'empty_cart', name='empty_cart'),
    url(r'^purchase/$', 'purchase', name='purchase'),
)

urlpatterns += patterns(
    'boxoffice.views',
    url(r'^boxoffice/$', 'box_office', name='box_office'),

    url(r'^boxoffice/event-categories/$', login_required(EventCategoryListing.as_view()), name='box_office_event_categories'),
    url(r'^boxoffice/new-event-category/$', login_required(EventCategoryCreate.as_view()), name='box_office_event_category_create'),
    url(r'^boxoffice/event-category/(?P<pk>[-\w\ ]+)/$', login_required(EventCategoryUpdate.as_view()), name='box_office_event_category'),
    url(r'^boxoffice/delete-event-category/(?P<pk>[-\w\ ]+)/$', login_required(EventCategoryDelete.as_view()), name='box_office_event_category_delete'),

    url(r'^boxoffice/events/$', login_required(EventListing.as_view()), name='box_office_events'),
    url(r'^boxoffice/new-event/$', login_required(EventCreate.as_view()), name='box_office_event_create'),
    url(r'^boxoffice/event/(?P<pk>[-\w\ ]+)/$', login_required(EventUpdate.as_view()), name='box_office_event'),
    url(r'^boxoffice/delete-event/(?P<pk>[-\w\ ]+)/$', login_required(EventDelete.as_view()), name='box_office_event_delete'),

    url(r'^boxoffice/buyers/$', login_required(BuyerListing.as_view()), name='box_office_buyers'),
    url(r'^boxoffice/new-buyer/$', login_required(BuyerCreate.as_view()), name='box_office_buyer_create'),
    url(r'^boxoffice/buyer/(?P<pk>[-\w\ ]+)/$', login_required(BuyerUpdate.as_view()), name='box_office_buyer'),
    url(r'^boxoffice/delete-buyer/(?P<pk>[-\w\ ]+)/$', login_required(BuyerDelete.as_view()), name='box_office_buyer_delete'),

)

urlpatterns += patterns(
    'django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'login.html'}, name='login'),
)
