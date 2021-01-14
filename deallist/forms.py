from django import forms
from .models import *
from .widgets import *

class DealListCreationForm(forms.ModelForm):
    company_name = forms.CharField(label='DD', widget=DatePickerWidget)

    class meta:
        model = ReceiptList
        fields = ['company_name']
        widgets = {
            'company_name': CounterTextInput,
            'receipt_date': DatePickerWidget,
        }
