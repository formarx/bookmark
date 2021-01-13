from django.urls import path
from .views import *

namespace = "deallist"
urlpatterns = [
    path('', DealListListView.as_view(), name='list'),
    # path('add/', DealCreateView.as_view(), name='add'),
    # path('detail/<int:pk>', DealDetailView.as_view(), name='detail'),
    # path('update/<int:pk>', DealUpdateView.as_view(), name='update'),
    # path('delete/<int:pk>', DealDeleteView.as_view(), name='delete'),
]
