from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('places.geojson', views.places_geojson, name='places_geojson'),
    path('places/<int:pk>/', views.place_detail_json, name='place_detail_json'),
]
