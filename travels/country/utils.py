from django.core.cache import cache
from django.db.models import Count

from .models import *

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить страну", 'url_name': 'add_page'},
    {'title': "Добавить континент", 'url_name': 'add_continent'},
    {'title': "Обратная связь", 'url_name': 'contact'},
]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Continent.objects.annotate(Count('country'))
            cache.set('cats', cats, 60)
        user_menu = menu.copy()  # Если пользователь не авторизован, то удаляется вторая запись
        if not self.request.user.is_authenticated:
            del user_menu[1:3]

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
