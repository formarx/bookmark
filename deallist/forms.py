from django import forms
from django.contrib.auth.models import User
from .models import ReceiptList
from .widgets import DatePickerWidget

# Must be changed!!
INVEST_CHOICES = [
    ('박영호', '박영호'),
    ('구경모', '구경모'),
    ('박형준', '박형준'),
]

class DealListCreationForm(forms.ModelForm):
    receipt_user = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=INVEST_CHOICES,
    )
    class Meta:
        model = ReceiptList
        fields = '__all__'
        widgets = {
            #'company_name': CounterTextInput,
            'receipt_date': DatePickerWidget,
        }
    
    def clean_receipt_user(self):
        cleaned_data = super().clean()
        ru = []
        for _ru in cleaned_data['receipt_user']:
            ru.append(User.objects.get(username=_ru))
        return ru
