from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from .models import *

# Create your views here.
class DealListListView(ListView):
    model = ReceiptList
    template_name = "deallist/list.html"
    paginate_by = 10
    ordering="-receipt_date"
