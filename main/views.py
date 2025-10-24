from django.shortcuts import render
from main.models import Place


def index(request):
    """Главная страница — отображение карты и списка мест."""
    return render(request, "main/index.html")

