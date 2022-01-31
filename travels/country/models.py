import string

from django.db import models
from django.urls import reverse


class Country(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название страны")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")  # blank=True может быть пустым
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")  # загрузка в эту папку по дате
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Время создания")  # Примет текущее время и не будет меняться
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время иземенения")  # Время будет меняться
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Continent', on_delete=models.PROTECT, verbose_name="Континент")  # Первичная модель как строка, чтобы не было ошибки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})  # Передает в url-шаблон post переменную post_slug

    class Meta:
        verbose_name = "Интересные страны"
        verbose_name_plural = "Интересные страны"
        ordering = ['-time_create', 'title']


class Continent(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название континента")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('continent', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Континент"
        verbose_name_plural = "Континенты"
        ordering = ["name"]
