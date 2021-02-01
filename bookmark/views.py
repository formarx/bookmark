from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from .models import Bookmark


# Create your views here.
class BookmarkListView(ListView):
    model = Bookmark
    paginate_by = 5
    ordering = "-id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['is_paginated']:
            context["min_page"] = min(context['page_obj'].number - 5, context['page_obj'].paginator.num_pages - 10)
            context["max_page"] = max(context['page_obj'].number + 5, 11)
        return context

class BookmarkCreateView(CreateView):
    model = Bookmark
    fields = ['site_name', 'url']
    success_url = reverse_lazy('bookmark:list')
    template_name_suffix = '_create'

class BookmarkDetailView(DetailView):
    model = Bookmark

class BookmarkUpdateView(UpdateView):
    model = Bookmark
    fields = ['site_name', 'url']
    template_name_suffix = '_update'

class BookmarkDeleteView(DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark:list')
