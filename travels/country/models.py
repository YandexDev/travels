import string

from django.db import models
from django.urls import reverse
from transliterate import translit


class Country(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Текст статьи")  # blank=True может быть пустым
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")  # загрузка в эту папку по дате
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")  # Примет текущее время и не будет меняться
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время иземенения")  # Время будет меняться
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Continent', on_delete=models.PROTECT, null=True, verbose_name="Континент")  # Первичная модель как строка, чтобы не было ошибки

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        title = ""
        for i in self.title:
            if i in string.ascii_letters:
                title += i
            else:
                title += translit(i, language_code='ru', reversed=True)
        return reverse('post', kwargs={'post_title': title})


class Continent(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название континента")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('continent', kwargs={'cat_id': self.pk})

