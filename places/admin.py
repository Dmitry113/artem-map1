from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from .models import Place, Image, Category


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    """Позволяет добавлять фотографии прямо на странице места и менять их порядок."""
    model = Image
    extra = 1
    fields = ('image', 'description', 'preview',)
    readonly_fields = ('preview',)
    verbose_name = "Фотография"
    verbose_name_plural = "Фотографии места"

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 100px; object-fit: contain;"/>', obj.image.url
            )
        return ""
    preview.short_description = "Превью"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    """Админка для места с сортируемыми фотографиями."""
    list_display = ('title', 'category', 'latitude', 'longitude', 'main_image_preview')
    search_fields = ('title', 'category__name')
    list_filter = ('category',)
    inlines = [ImageInline]
    readonly_fields = ('main_image_preview',)

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="height: 150px; object-fit: contain;"/>', obj.main_image.url
            )
        return ""
    main_image_preview.short_description = "Превью главного изображения"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'description', 'preview')
    search_fields = ('place__title', 'description')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 100px; object-fit: contain;"/>', obj.image.url
            )
        return ""
    preview.short_description = "Превью"
