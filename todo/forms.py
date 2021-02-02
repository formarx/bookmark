from django import forms
from deallist.widgets import DatePickerWidget

from .models import TodoList

class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ('title', 'content', 'end_date')
        widgets = {
            'end_date' : DatePickerWidget
        }
