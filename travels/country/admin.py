from django.contrib import admin
from django.utils.safestring import mark_safe

from country.models import *


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'population', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title', 'get_html_photo')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')  # В поле редактирования
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')  # Только для чтения
    # save_on_top = True  # Дублирует строку о сохраниении вверху

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{ object.photo.url }" width=70>')

    get_html_photo.short_description = "Миниатрюра"


class ContinentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Country, CountryAdmin)
admin.site.register(Continent, ContinentAdmin)

admin.site.site_title = 'Админ-панель сайта о путешествиях'
admin.site.site_header = 'Админ-панель сайта о путешествиях'