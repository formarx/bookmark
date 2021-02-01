# deallist/view.py
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.urls import reverse_lazy

from .models import ReceiptList
from .forms import DealListCreationForm

# Create your views here.
class DealListListView(ListView):
    model = ReceiptList
    template_name = "deallist/list.html"
    paginate_by = 3
    ordering=['-receipt_date', '-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['is_paginated']:
            context["min_page"] = min(context['page_obj'].number - 5, context['page_obj'].paginator.num_pages - 10)
            context["max_page"] = max(context['page_obj'].number + 5, 11)
        return context

class DealListCreateView(CreateView):
    model = ReceiptList
    #fields = '__all__'
    success_url = reverse_lazy('deallist:list')
    form_class = DealListCreationForm
    template_name = 'deallist/create.html'


class DealListDetailView(DetailView):
    model = ReceiptList

class DealListUpdateView(UpdateView):
    model = ReceiptList
    #fields = '__all__'
    #template_name_suffix = '_update'
    template_name = 'deallist/create.html'
    success_url = reverse_lazy('deallist:list')
    form_class = DealListCreationForm

class DealListDeleteView(DeleteView):
    model = ReceiptList
    success_url = reverse_lazy('deallist:list')
