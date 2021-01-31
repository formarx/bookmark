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
    paginate_by = 30
    ordering=['-receipt_date', '-id']


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
