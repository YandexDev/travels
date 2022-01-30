from django.urls import path, re_path

from country.views import *

urlpatterns = [
    path('', index, name="homepage"),
    path('about/', about, name="about"),
    path('addpage/', addpage, name="add_page"),
    path('contact/', contact, name="contact"),
    path('login/', login, name="login"),
    path('post/<slug:post_slug>/', show_post, name="post"),
    path('continent/<slug:cat_slug>/', show_continent, name="continent"),

    path('country/', list_country),
    path('country/<slug:country>/', name_country),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),  # Регулярные выражения
]
