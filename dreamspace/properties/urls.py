from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:property_id>/', views.property_detail, name='property_detail'),
    path('properties/type/<int:property_type_id>/', views.property_list_by_type, name='property_list_by_type'),
    path('about', views.about, name='about'),
    path('search/', views.search_results, name='search_results'),
    path('contact/', views.contact, name='contact'),
    path('contact_success/', views.contact_success, name='contact_success'),
]
