from django.forms import ModelForm
from ticketing.models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
