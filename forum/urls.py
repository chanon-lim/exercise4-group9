from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
    path('post/', views.post_create, name='post_create'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('comment/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]
