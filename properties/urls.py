from django.urls import path
from .views import (PropertyListView,PropertyDetailView,home,about,contact,)
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('properties/', PropertyListView.as_view(), name='property_list'),
    path('properties/<int:pk>/', PropertyDetailView.as_view(), name='property_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('properties/add/', views.add_property, name='add_property'),
    path('properties/edit/<int:pk>/', views.edit_property, name='edit_property'),
]