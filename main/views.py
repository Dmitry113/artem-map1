from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from places.models import Place  # убедись, что импорт из places

def index(request):
    return render(request, "main/index.html")


def places_geojson(request):
    """Возвращает все места в формате GeoJSON для карты"""
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
                "title": place.title,
                "detailsUrl": f"/places/{place.id}/",
            },
        })
    return JsonResponse({"type": "FeatureCollection", "features": features})


def place_detail_json(request, pk):
    """Возвращает полные данные о месте для сайдбара"""
    place = get_object_or_404(Place.objects.prefetch_related('images'), pk=pk)

    main_url = place.main_image.url if place.main_image else None
    gallery_urls = [img.image.url for img in place.images.all() if img.image]

    if main_url in gallery_urls:
        gallery_urls.remove(main_url)

    # Если краткое описание пустое, используем первые 200 символов полного описания
    short_desc = place.short_description.strip() or (place.description[:200] if place.description else "")

    data = {
        "title": place.title,
        "short_description": short_desc,
        "long_description": place.description or "",
        "main_image": main_url or "",
        "images": gallery_urls,
    }
    return JsonResponse(data)
