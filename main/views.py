from django.shortcuts import render
from main.models import Place

def home(request):
    """Главная страница с отображением всех мест и их фотографий."""
    places = Place.objects.prefetch_related("images").all()
    return render(request, "main/home.html", {"places": places})
