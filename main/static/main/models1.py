from django.db import models


class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField('Название места', max_length=200)
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='places'
    )
    main_image = models.ImageField(
        'Главное изображение',
        upload_to='places/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        ordering = ['name']

    def __str__(self):
        return self.name


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        verbose_name='Место',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='places/gallery/'
    )
    description = models.CharField(
        'Описание изображения',
        max_length=255,
        blank=True
    )

    class Meta:
        verbose_name = 'Изображение места'
        verbose_name_plural = 'Изображения мест'

    def __str__(self):
        return f"Фото для {self.place.name}"
