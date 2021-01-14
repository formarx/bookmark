from django import forms
from .models import ReceiptList
from .widgets import DatePickerWidget

class DealListCreationForm(forms.ModelForm):
    class Meta:
        model = ReceiptList
        fields = '__all__'
        widgets = {
            #'company_name': CounterTextInput,
            'receipt_date': DatePickerWidget,
        }
