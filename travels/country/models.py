from django.db import models


class Country(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)  # blank=True может быть пустым
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")  # загрузка в эту папку по дате
    time_create = models.DateTimeField(auto_now_add=True)  # Примет текущее время и не будет меняться
    time_update = models.DateTimeField(auto_now=True)  # Время будет меняться
    is_published = models.BooleanField(default=True)
