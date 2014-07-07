from django import forms
from django.forms import ModelForm
from ticketing.models import Event
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings


class EventForm(ModelForm):

    class Meta:
        model = Event

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_method = 'post'
        self.fields['date'].input_formats=(settings.DATE_INPUT_FORMATS)
        self.helper.add_input(Submit('submit', 'Save Event', css_class="col-sm-offset-4 btn-success"))
        

