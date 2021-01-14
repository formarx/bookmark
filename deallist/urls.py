from django.urls import path
from .views import *
from .dump import *

app_name = "deallist"
urlpatterns = [
    path('', DealListListView.as_view(), name='list'),
    path('add/', DealListCreateView.as_view(), name='add'),
    path('detail/<int:pk>', DealListDetailView.as_view(), name='detail'),
    path('update/<int:pk>', DealListUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', DealListDeleteView.as_view(), name='delete'),
    path('dump', dump, name='dump'),
]
