from django.urls import path, re_path

from country.views import *

urlpatterns = [
    path('', index, name="homepage"),
    path('country/', list_country),
    path('country/<slug:country>/', name_country),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),  # Регулярные выражения
]
