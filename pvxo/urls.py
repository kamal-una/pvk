from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from boxoffice.views import EventListing, EventCreate, EventUpdate, EventDelete
from boxoffice.views import BuyerListing, BuyerCreate, BuyerUpdate, BuyerDelete
from boxoffice.views import EventCategoryListing, EventCategoryCreate, EventCategoryUpdate, EventCategoryDelete
from boxoffice.views import FacilityListing, FacilityCreate, FacilityUpdate, FacilityDelete
from boxoffice.views import PaymentTypeListing, PaymentTypeCreate, PaymentTypeUpdate, PaymentTypeDelete
from boxoffice.views import PriceCategoryListing, PriceCategoryCreate, PriceCategoryUpdate, PriceCategoryDelete
from boxoffice.views import PriceMatrixListing, PriceMatrixCreate, PriceMatrixUpdate, PriceMatrixDelete
from boxoffice.views import PriceListing, PriceCreate, PriceUpdate, PriceDelete
from boxoffice.views import TransactionListing

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

    url(r'^boxoffice/facilities/$', login_required(FacilityListing.as_view()), name='box_office_facilities'),
    url(r'^boxoffice/new-facility/$', login_required(FacilityCreate.as_view()), name='box_office_facility_create'),
    url(r'^boxoffice/facility/(?P<pk>[-\w\ ]+)/$', login_required(FacilityUpdate.as_view()), name='box_office_facility'),
    url(r'^boxoffice/delete-facility/(?P<pk>[-\w\ ]+)/$', login_required(FacilityDelete.as_view()), name='box_office_facility_delete'),

    url(r'^boxoffice/payment-types/$', login_required(PaymentTypeListing.as_view()), name='box_office_payment_types'),
    url(r'^boxoffice/new-payment-type/$', login_required(PaymentTypeCreate.as_view()), name='box_office_payment_type_create'),
    url(r'^boxoffice/payment-type/(?P<pk>[-\w\ ]+)/$', login_required(PaymentTypeUpdate.as_view()), name='box_office_payment_type'),
    url(r'^boxoffice/delete-payment-type/(?P<pk>[-\w\ ]+)/$', login_required(PaymentTypeDelete.as_view()), name='box_office_payment_type_delete'),

    url(r'^boxoffice/price-categories/$', login_required(PriceCategoryListing.as_view()), name='box_office_price_categories'),
    url(r'^boxoffice/new-price-category/$', login_required(PriceCategoryCreate.as_view()), name='box_office_price_category_create'),
    url(r'^boxoffice/price-category/(?P<pk>[-\w\ ]+)/$', login_required(PriceCategoryUpdate.as_view()), name='box_office_price_category'),
    url(r'^boxoffice/delete-price-category/(?P<pk>[-\w\ ]+)/$', login_required(PriceCategoryDelete.as_view()), name='box_office_price_category_delete'),

    url(r'^boxoffice/price-matrices/$', login_required(PriceMatrixListing.as_view()), name='box_office_price_matrices'),
    url(r'^boxoffice/new-price-matrix/$', login_required(PriceMatrixCreate.as_view()), name='box_office_price_matrix_create'),
    url(r'^boxoffice/price-matrix/(?P<pk>[-\w\ ]+)/$', login_required(PriceMatrixUpdate.as_view()), name='box_office_price_matrix'),
    url(r'^boxoffice/delete-price-matrix/(?P<pk>[-\w\ ]+)/$', login_required(PriceMatrixDelete.as_view()), name='box_office_price_matrix_delete'),

    url(r'^boxoffice/prices/$', login_required(PriceListing.as_view()), name='box_office_prices'),
    url(r'^boxoffice/new-price/$', login_required(PriceCreate.as_view()), name='box_office_price_create'),
    url(r'^boxoffice/price/(?P<pk>[-\w\ ]+)/$', login_required(PriceUpdate.as_view()), name='box_office_price'),
    url(r'^boxoffice/delete-price/(?P<pk>[-\w\ ]+)/$', login_required(PriceDelete.as_view()), name='box_office_price_delete'),

    url(r'^boxoffice/transactions/$', login_required(TransactionListing.as_view()), name='box_office_transactions'),
    url(r'^boxoffice/transaction/(?P<pk>[-\w\ ]+)/$', 'transaction_details', name='box_office_transaction'),

    url(r'^boxoffice/seat/(?P<pk>[-\w\ ]+)/$', 'seat_details', name='box_office_seat'),

    url(r'^boxoffice/event-summary/$', 'event_summary', name='box_office_event_summary'),

)

urlpatterns += patterns(
    'django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'login.html'}, name='login'),
)
