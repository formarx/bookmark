from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    path('', views.home, name='home'),
    path('boards/<slug:board_slug>/', views.post_list, name='post_list'),
    path('boards/<slug:board_slug>/posts/new/', views.new_post, name='new_post'),
    path('posts/<int:post_id>/', views.view_post, name='view_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/history/', views.post_history_list, name='post_history_list'),
    path('posts/<int:post_id>/comments/', views.comment_list, name='comment_list'),
    path('posts/<int:post_id>/comments/new/', views.new_comment, name='new_comment'),
    path('posts/<int:post_id>/comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('posts/<int:post_id>/appr/<int:appr_id>/edit/', views.edit_appr, name='edit_appr'),
]
