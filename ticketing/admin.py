from django.contrib import admin

# Register your models here.
from ticketing.models import Facility, FacilitySeat, BuyerType, BuyerGroup, BuyerGroupMapping, PriceMatrix, \
    PriceCategory, Price, EventRun, EventCategory, PaymentType, Event, EventBuyerMapping, CustomUser, Transaction, Seat


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'seated', 'number_of_seats', 'created', 'last_update')
    search_fields = ('name',)


class FacilitySeatAdmin(admin.ModelAdmin):
    list_display = ('facility', 'section', 'row', 'seat')


class BuyerGroupAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


class BuyerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


class BuyerGroupMappingAdmin(admin.ModelAdmin):
    list_display = ('buyer_group', 'buyer_type')
    search_fields = ('buyer_group', 'buyer_type')


class PriceMatrixAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


class PriceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PriceAdmin(admin.ModelAdmin):
    list_display = ('matrix', 'category', 'buyer_type', 'price')
    search_fields = ('matrix', 'category', 'buyer_type', 'price')


class EventRunAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'run', 'facility', 'date', 'sale_start', 'sale_end', 'image_url', 'doors_open', 'product_id', 'min_tickets', 'max_tickets', 'information')
    search_fields = ('name', 'category', 'run', 'facility', 'date', 'product_id')


class EventBuyerMappingAdmin(admin.ModelAdmin):
    list_display = ('event', 'buyer_type')
    search_fields = ('event', 'buyer_type')


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'title', 'first_name', 'last_name', 'date_joined', 'last_update')
    search_fields = ('first_name', 'last_name', 'email')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'user')
    search_fields = ('date', 'user')


class SeatAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'event', 'seat', 'buyer_type', 'payment_type', 'user', 'price', 'payment_amount', 'status')
    search_fields = ('transaction', 'event', 'seat', 'buyer_type', 'status')

admin.site.register(BuyerType, BuyerTypeAdmin)
admin.site.register(BuyerGroup, BuyerGroupAdmin)
admin.site.register(BuyerGroupMapping, BuyerGroupMappingAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(FacilitySeat, FacilitySeatAdmin)
admin.site.register(PriceMatrix, PriceMatrixAdmin)
admin.site.register(PriceCategory, PriceCategoryAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(EventRun, EventRunAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(PaymentType, PaymentTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventBuyerMapping, EventBuyerMappingAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Seat, SeatAdmin)
