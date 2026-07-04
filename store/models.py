from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

class Model(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

class Type(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

class Place(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)


class Phone(models.Model):
    class QualityClass(models.TextChoices):
        ORIGINAL = 'ORIG', 'Оригинал (PRC)'
        HIGH_COPY = 'H_CPY', 'Высокое качество (High Copy)'
        COPY = 'COPY', 'Копия'
        USED = 'USED', 'Б/У (Разбор)'


    name = models.CharField(max_length=100, verbose_name='Название')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд')
    model = models.ForeignKey(Model, on_delete=models.CASCADE, verbose_name='Модель')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name='Тип')
    quality = models.CharField(max_length=10,
                               choices=QualityClass.choices,
                               default=QualityClass.HIGH_COPY,
                               verbose_name='Качество')
    sku = models.IntegerField(verbose_name='Артикул')
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Актуальная цена')
    availability = models.BooleanField(default=True, verbose_name='Наличие')
    image = models.ImageField(blank=True ,null=True, verbose_name='Изображение')
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество на складе"
    )
    made_in = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='part_place', null=True, verbose_name='Место производства')

