from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
import logging
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

@login_required
def box_office(request):
    context = {}

    html = render(request, 'ticketing/box_office.html', context)
    return StreamingHttpResponse(html)

"""
Event Categories
"""
from forms import EventCategoryForm
from ticketing.models import EventCategory

class EventCategoryListing(ListView):
    model = EventCategory
    paginate_by = 20

class EventCategoryCreate(CreateView):
    form_class = EventCategoryForm
    model = EventCategory

    def get_success_url(self):
        return reverse('box_office_event_categories')

class EventCategoryUpdate(UpdateView):
    form_class = EventCategoryForm
    model = EventCategory

    def get_success_url(self):
        return reverse('box_office_event_categories')

class EventCategoryDelete(DeleteView):
    model = EventCategory

    def get_success_url(self):
        return reverse('box_office_event_categories')

"""
Events
"""
from forms import EventForm
from ticketing.models import Event

class EventListing(ListView):
    model = Event
    paginate_by = 20

class EventCreate(CreateView):
    model = Event
    form_class = EventForm

    def get_success_url(self):
        return reverse('box_office_events')

class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm

    def get_success_url(self):
        return reverse('box_office_events')

class EventDelete(DeleteView):
    model = Event

    def get_success_url(self):
        return reverse('box_office_events')

"""
Buyers
"""
from forms import BuyerForm
from ticketing.models import BuyerType

class BuyerListing(ListView):
    model = BuyerType
    paginate_by = 20

class BuyerCreate(CreateView):
    model = BuyerType
    form_class = BuyerForm

    def get_success_url(self):
        return reverse('box_office_buyers')

class BuyerUpdate(UpdateView):
    model = BuyerType
    form_class = BuyerForm

    def get_success_url(self):
        return reverse('box_office_buyers')

class BuyerDelete(DeleteView):
    model = BuyerType

    def get_success_url(self):
        return reverse('box_office_buyers')

"""
Facilities
"""
from forms import FacilityForm
from ticketing.models import Facility

class FacilityListing(ListView):
    model = Facility
    paginate_by = 20

class FacilityCreate(CreateView):
    model = Facility
    form_class = FacilityForm

    def get_success_url(self):
        return reverse('box_office_facilities')

class FacilityUpdate(UpdateView):
    model = Facility
    form_class = FacilityForm

    def get_success_url(self):
        return reverse('box_office_facilities')

class FacilityDelete(DeleteView):
    model = Facility

    def get_success_url(self):
        return reverse('box_office_facilities')


"""
Facilities
"""
from forms import PaymentTypeForm
from ticketing.models import PaymentType

class PaymentTypeListing(ListView):
    model = PaymentType
    paginate_by = 20

class PaymentTypeCreate(CreateView):
    model = PaymentType
    form_class = PaymentTypeForm

    def get_success_url(self):
        return reverse('box_office_payment_types')

class PaymentTypeUpdate(UpdateView):
    model = PaymentType
    form_class = PaymentTypeForm

    def get_success_url(self):
        return reverse('box_office_payment_types')

class PaymentTypeDelete(DeleteView):
    model = PaymentType

    def get_success_url(self):
        return reverse('box_office_payment_types')


"""
Price Categories
"""
from forms import PriceCategoryForm
from ticketing.models import PriceCategory

class PriceCategoryListing(ListView):
    model = PriceCategory
    paginate_by = 20

class PriceCategoryCreate(CreateView):
    model = PriceCategory
    form_class = PriceCategoryForm

    def get_success_url(self):
        return reverse('box_office_price_categories')

class PriceCategoryUpdate(UpdateView):
    model = PriceCategory
    form_class = PriceCategoryForm

    def get_success_url(self):
        return reverse('box_office_price_categories')

class PriceCategoryDelete(DeleteView):
    model = PriceCategory

    def get_success_url(self):
        return reverse('box_office_price_categories')


"""
Price Matrices
"""
from forms import PriceMatrixForm
from ticketing.models import PriceMatrix

class PriceMatrixListing(ListView):
    model = PriceMatrix
    paginate_by = 20

class PriceMatrixCreate(CreateView):
    model = PriceMatrix
    form_class = PriceMatrixForm

    def get_success_url(self):
        return reverse('box_office_price_matrices')

class PriceMatrixUpdate(UpdateView):
    model = PriceMatrix
    form_class = PriceMatrixForm

    def get_success_url(self):
        return reverse('box_office_price_matrices')

class PriceMatrixDelete(DeleteView):
    model = PriceMatrix

    def get_success_url(self):
        return reverse('box_office_price_matrices')


"""
Prices
"""
from forms import PriceForm
from ticketing.models import Price

class PriceListing(ListView):
    model = Price
    paginate_by = 20

class PriceCreate(CreateView):
    model = Price
    form_class = PriceForm

    def get_success_url(self):
        return reverse('box_office_prices')

class PriceUpdate(UpdateView):
    model = Price
    form_class = PriceForm

    def get_success_url(self):
        return reverse('box_office_prices')

class PriceDelete(DeleteView):
    model = Price

    def get_success_url(self):
        return reverse('box_office_prices')


"""
Transactions
"""
from forms import TransactionForm
from ticketing.models import Transaction, Seat

class TransactionListing(ListView):
    model = Transaction
    paginate_by = 20

def transaction_details(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    form = TransactionForm(instance=transaction)
    seats = Seat.history.filter(transaction=transaction).order_by('seat')

    seats = sorted(seats, key=lambda mapping: [mapping.seat.section,
                                               mapping.seat.row,
                                               mapping.seat.seat])

    context = {'form': form,
               'transaction': transaction,
               'seats': seats}

    html = render(request, 'ticketing/transaction_form.html', context)
    return StreamingHttpResponse(html)

def seat_details(request, pk):
    seats = Seat.history.filter(id=pk)

    seats = sorted(seats, key=lambda mapping: [mapping.transaction.date], reverse=True)

    logging.info('number of records found: %s', (len(seats)))

    context = {'seats': seats}

    html = render(request, 'ticketing/event_seat_details.html', context)
    return StreamingHttpResponse(html)

"""
Event Summary
"""
def event_summary(request):
    events = Event.objects.all()

    context = {'events': events}

    html = render(request, 'ticketing/event_summary.html', context)
    return StreamingHttpResponse(html)
