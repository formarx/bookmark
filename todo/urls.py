from django.urls import path
from . import views

app_name = "todo"
urlpatterns = [
    path('', views.Todo_ListView.as_view(), name='plist'),
    path('list/<int:pcode>', views.Todo_ListView.as_view(), name='list'),
    path('insert/<int:pcode>', views.check_post, name='insert'),
    path('save_priority/', views.save_priority, name='save_priority'),
    path('is_complete/', views.is_complete, name='is_complete'),
    path('is_non_complete/', views.is_non_complete, name='is_non_complete'),
    path('detail/<int:pk>', views.Todo_DetailView.as_view(), name='detail'),
    path('update/<int:pk>', views.Todo_UpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.Todo_DeleteView.as_view(), name='delete'),
]
