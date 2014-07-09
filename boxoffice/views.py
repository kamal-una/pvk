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

    html = render(request, 'box_office.html', context)
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








