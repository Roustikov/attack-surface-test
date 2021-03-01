from django.urls import path

from . import views

urlpatterns = [
    path('attack', views.attack, name='attack'),
    path('stats', views.stats, name='stats'),
]
