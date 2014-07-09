from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
import logging
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from forms import EventForm, BuyerForm
from ticketing.models import EventCategory, Event, BuyerType


@login_required
def box_office(request):
    context = {}

    html = render(request, 'box_office.html', context)
    return StreamingHttpResponse(html)


class EventCategoryListing(ListView):
    model = EventCategory
    paginate_by = 20

class EventCategoryCreate(CreateView):
    form_class = BuyerForm
    model = EventCategory

    def get_success_url(self):
        return reverse('box_office_event_categories')

class EventCategoryUpdate(UpdateView):
    form_class = BuyerForm
    model = EventCategory

    def get_success_url(self):
        return reverse('box_office_event_categories')

class EventCategoryDelete(DeleteView):
    model = EventCategory

    def get_success_url(self):
        return reverse('box_office_event_categories')


class EventListing(ListView):
    model = Event
    paginate_by = 20

class EventCreate(CreateView):
    form_class = EventForm
    model = Event

    def get_success_url(self):
        return reverse('box_office_events')

class EventUpdate(UpdateView):
    form_class = EventForm
    model = Event

    def get_success_url(self):
        return reverse('box_office_events')

class EventDelete(DeleteView):
    model = Event

    def get_success_url(self):
        return reverse('box_office_events')


class BuyerListing(ListView):
    model = BuyerType
    paginate_by = 20

class BuyerCreate(CreateView):
    form_class = BuyerForm
    model = BuyerType

    def get_success_url(self):
        return reverse('box_office_buyers')

class BuyerUpdate(UpdateView):
    form_class = BuyerForm
    model = BuyerType

    def get_success_url(self):
        return reverse('box_office_buyers')

class BuyerDelete(DeleteView):
    model = BuyerType

    def get_success_url(self):
        return reverse('box_office_buyers')





