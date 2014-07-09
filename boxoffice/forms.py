from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings

from ticketing.models import Event
from ticketing.models import BuyerType
from ticketing.models import EventCategory
from ticketing.models import Facility
from ticketing.models import PaymentType
from ticketing.models import PriceCategory
from ticketing.models import PriceMatrix
from ticketing.models import Price


class BootstrapMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save', css_class="col-sm-offset-4 btn-success"))


class EventForm(BootstrapMixin, ModelForm):
    class Meta:
        model = Event


class BuyerForm(BootstrapMixin, ModelForm):
    class Meta:
        model = BuyerType


class EventCategoryForm(BootstrapMixin, ModelForm):
    class Meta:
        model = EventCategory


class FacilityForm(BootstrapMixin, ModelForm):
    class Meta:
        model = Facility


class PaymentTypeForm(BootstrapMixin, ModelForm):
    class Meta:
        model = PaymentType


class PriceCategoryForm(BootstrapMixin, ModelForm):
    class Meta:
        model = PriceCategory


class PriceMatrixForm(BootstrapMixin, ModelForm):
    class Meta:
        model = PriceMatrix


class PriceForm(BootstrapMixin, ModelForm):
    class Meta:
        model = Price
