from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('display_all', views.display_all),
    path('display_one/<int:id>', views.display_one),
    path('create', views.create),
    path('first_name/<int:id>', views.first_name),
    path('like/<int:id>', views.liked_ideas),
    path('user/<int:id>', views.one_user),
    path('delete/<int:id>', views.delete),
]