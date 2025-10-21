from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Place, PlaceImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'


class PlaceImageInline(admin.TabularInline):
    """Встраиваемая форма для изображений внутри карточки места"""
    model = PlaceImage
    extra = 1
    fields = ('image', 'description', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius:6px;">', obj.image.url)
        return "—"
    preview.short_description = "Превью"


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description_short', 'main_image_preview')
    search_fields = ('name', 'description')
    list_filter = ('category',)
    ordering = ('name',)
    inlines = [PlaceImageInline]

    def description_short(self, obj):
        return (obj.description[:60] + '...') if len(obj.description) > 60 else obj.description
    description_short.short_description = 'Описание'

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" width="70" style="border-radius:8px;">', obj.main_image.url)
        return "—"
    main_image_preview.short_description = 'Главное фото'


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'description', 'image_preview')
    search_fields = ('place__name', 'description')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="70" style="border-radius:8px;">', obj.image.url)
        return "—"
    image_preview.short_description = 'Изображение'
