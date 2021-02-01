from django.urls import path
from . import views

app_name = "todo"
urlpatterns = [
    path('', views.Todo_list.as_view(), name='plist'),
    path('list/<int:pcode>', views.Todo_list.as_view(), name='list'),
    path('insert/', views.check_post, name='insert'),
    path('save_priority/', views.check_post, name='save_priority'),
    path('is_complete/', views.check_post, name='is_complete'),
    path('is_non_complete/', views.check_post, name='is_non_complete'),
    path('detail/<int:pk>', views.check_post, name='detail'),
]
