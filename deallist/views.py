from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.urls import reverse_lazy

from .models import *

# Create your views here.
class DealListListView(ListView):
    model = ReceiptList
    template_name = "deallist/list.html"
    paginate_by = 30
    ordering="-receipt_date"


class DealListCreateView(CreateView):
    model = ReceiptList
    fields = ['receipt_date', 'receipt_user', 'company_name', 'sourcing', 'company_field', 'memo', 'is_invest']
    success_url = reverse_lazy('list')
    template_name = 'deallist/create.html'

class DealListDetailView(DetailView):
    model = ReceiptList

class DealListUpdateView(UpdateView):
    model = ReceiptList
    fields = ['receipt_date', 'receipt_user', 'company_name', 'sourcing', 'company_field', 'memo','is_invest']
    template_name_suffix = '_update'
    success_url = reverse_lazy('list')

class DealListDeleteView(DeleteView):
    model = ReceiptList
    success_url = reverse_lazy('list')