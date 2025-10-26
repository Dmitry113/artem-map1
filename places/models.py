from django.db import models
from django.utils.html import mark_safe


class Category(models.Model):
    """Категория места — парк, музей, двор, кафе и т.п."""
    name = models.CharField(max_length=100, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Place(models.Model):
    """Основная модель для описания интересных мест."""
    title = models.CharField(max_length=200, verbose_name="Название места")
    short_description = models.TextField(verbose_name="Краткое описание", blank=True)
    description = models.TextField(verbose_name="Полное описание", blank=True)
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    main_image = models.ImageField(
        upload_to="places_main/",
        verbose_name="Главное изображение",
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="places",
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title

    def main_image_preview(self):
        """Миниатюра главного изображения для админки."""
        if self.main_image:
            return mark_safe(f'<img src="{self.main_image.url}" style="height:100px;"/>')
        return ""
    main_image_preview.short_description = "Превью главного изображения"


class Image(models.Model):
    """Фотографии, связанные с местом."""
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Место"
    )
    image = models.ImageField(upload_to="places_gallery/", verbose_name="Фотография")
    description = models.CharField(max_length=255, verbose_name="Описание", blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")  # <-- новое поле

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"
        ordering = ['order']  # сортировка по этому полю

    def __str__(self):
        return f"Фото {self.id} для {self.place.title}"

    def preview(self):
        """Возвращает HTML для миниатюры в админке."""
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="height:100px;"/>')
        return ""
    preview.short_description = "Превью"
