from django.db import models


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
    description = models.TextField(verbose_name="Описание", blank=True)
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
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


class Image(models.Model):
    """Фотографии, связанные с местом."""
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Место"
    )
    image = models.ImageField(upload_to="places_images/", verbose_name="Фотография")
    description = models.CharField(max_length=255, verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return f"Фото {self.id} для {self.place.title}"

