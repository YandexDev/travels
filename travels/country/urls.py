from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from country.views import *

urlpatterns = [
    # path('', cache_page(60)(CountryHome.as_view()), name="homepage"),  # Кэширование на уровне представлений
    path('', CountryHome.as_view(), name="homepage"),
    path('about/', About.as_view(), name="about"),
    path('addpage/', AddPage.as_view(), name="add_page"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_user, name="logout"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name="post"),
    path('continent/<slug:cat_slug>/', CountryContinent.as_view(), name="continent"),

    path('contact/', contact, name="contact"),
    # path('country/', list_country),
    # path('country/<slug:country>/', name_country),
    # re_path(r'^archive/(?P<year>[0-9]{4})/', archive),  # Регулярные выражения
]
