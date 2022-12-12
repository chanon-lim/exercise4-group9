from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
    path('submit/', views.submit, name='submit'),
    path('post/<post_id>/', views.detailed_post, name='detailed_post'),
]