from django.urls import path, re_path

from country.views import *

urlpatterns = [
    path('', CountryHome.as_view(), name="homepage"),
    path('about/', About.as_view(), name="about"),
    path('addpage/', AddPage.as_view(), name="add_page"),
    path('contact/', contact, name="contact"),
    path('login/', login, name="login"),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name="post"),
    path('continent/<slug:cat_slug>/', CountryContinent.as_view(), name="continent"),

    path('country/', list_country),
    path('country/<slug:country>/', name_country),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),  # Регулярные выражения
]
