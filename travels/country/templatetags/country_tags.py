from django import template
from country.models import *

register = template.Library()


@register.simple_tag(name='getcont')
def get_continents(filter=None):
    if not filter:
        return Continent.objects.all()
    else:
        return Continent.objects.filter(pk=filter)
# В шаблоне - {% getcont filter=1 %} или {% getcont 1 %}


@register.inclusion_tag('country/list_continents.html')
def show_continents(sort=None, cat_selected=0):
    if not sort:
        conts = Continent.objects.all()
    else:
        conts = Continent.objects.order_by(sort)
    return {'conts': conts, 'cat_selected': cat_selected}
