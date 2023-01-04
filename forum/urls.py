from django.urls import path

from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
    path('<tag_slug>', views.tag_view, name='tag_view'),
    path('post/', views.post_create, name='post_create'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/like/', views.post_like, name='post_like'),
    path(
        'comment/<int:comment_id>/delete',
        views.comment_delete,
        name='comment_delete',
    ),
    path(
        'comment/<int:comment_id>/like',
        views.comment_like,
        name='comment_like'
    )
]
