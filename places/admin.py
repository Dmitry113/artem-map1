from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Place, Image, Category


# ----------------- Форма с CKEditor для Place -----------------
class PlaceAdminForm(forms.ModelForm):
    short_description = forms.CharField(
        widget=CKEditorWidget(),
        required=False,
        label="Краткое описание"
    )
    description = forms.CharField(
        widget=CKEditorWidget(),
        required=False,
        label="Полное описание"
    )

    class Meta:
        model = Place
        fields = '__all__'


# ----------------- Inline для фотографий -----------------
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


# ----------------- Админка Place -----------------
@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    form = PlaceAdminForm  # Подключаем форму с CKEditor
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


# ----------------- Админка Category -----------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ----------------- Админка Image -----------------
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
