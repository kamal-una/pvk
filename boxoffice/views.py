from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
import logging

from forms import EventForm
from ticketing.models import Event


@login_required
def box_office(request):
    context = {}

    html = render(request, 'box_office.html', context)
    return StreamingHttpResponse(html)


def box_office_event(request, event=None):
    if event:
        event = get_object_or_404(Event, pk=event)
        show_delete = True
    else:
        event = Event()
        show_delete = False

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()

    form = EventForm(instance=event)
    context = {}

    html = render(request, 'box_office_event.html', context)
    return StreamingHttpResponse(html)


@login_required
def box_office_event_delete(request, event=None):
    if event:
        event = get_object_or_404(Event, pk=int(event))
        event.delete()
        return redirect('box_office')