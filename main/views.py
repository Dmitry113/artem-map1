from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from main.models import Place


def index(request):
    return render(request, "main/index.html")


def places_geojson(request):
    features = []
    for place in Place.objects.all():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude],
            },
            "properties": {
                "id": place.id,
                "title": place.name,
                "detailsUrl": f"/places/{place.id}/",
            },
        })
    return JsonResponse({"type": "FeatureCollection", "features": features})


def place_detail_json(request, pk):
    """Шаг №11 — API возвращает полные данные о месте"""
    place = get_object_or_404(Place.objects.prefetch_related('images'), pk=pk)

    main_url = place.main_image.url if place.main_image else None
    gallery_urls = [img.image.url for img in place.images.all() if img.image]

    # Убираем дубликаты
    if main_url in gallery_urls:
        gallery_urls.remove(main_url)

    data = {
        "title": place.name,
        "short_description": getattr(place, "short_description", "") or "",
        "long_description": place.description or "",
        "main_image": main_url or "",
        "images": gallery_urls,
    }
    return JsonResponse(data)
