from django.urls import path
from django.views.generic.detail import DetailView

from .views import *

app_name = 'photo'
urlpatterns = [
    path('', photo_list, name='list'),
    path('detail/<int:pk>/', DetailView.as_view(model=Photo, template_name='photo/detail.html'), name='detail'),
    path('upload/', PhotoUploadView.as_view(), name='upload'),
    path('update/<int:pk>/', PhotoUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PhotoDeleteView.as_view(), name='delete'),
]
