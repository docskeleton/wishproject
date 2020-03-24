from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('wishes', views.dashboard),
    path('wishes/new', views.create),
    path('wishes/edit/<int:wish_id>', views.editwish),
    path('wishes/stats', views.stats),
    # redirects
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('create_wish', views.create_wish),
    path('edit_wish/<int:wish_id>', views.edit),
    path('remove_wish/<int:wish_id>', views.delete),
    path('grant_wish/<int:wish_id>', views.granted_wish),
    path('like/<int:wish_id>', views.like_wish),
]







