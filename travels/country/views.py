from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from country.models import Country

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]


def index(request):
    posts = Country.objects.all()
    return render(request, 'country/index.html', {'posts': posts, 'menu': menu, 'title': 'Главная страница'})


def about(request):
    return render(request, 'country/about.html', {'menu': menu, 'title': 'О сайте'})


def list_country(request):
    return HttpResponse("<h1>Страница со списком стран</h1>")


def name_country(request, country):
    if request.GET:  # http://127.0.0.1:8000/country/russia/?name=Russia&type=Cold
        print(request.GET)  # <QueryDict: {'name': ['Russia'], 'type': ['Cold']}>
    return HttpResponse(f"<h1>Описание страны {country}</h1>")


def archive(request, year):
    if int(year) < 1986 or int(year) > 2022:
        # raise Http404()  Выбросит ошибку 404
        # return redirect("/")  # Редирект на главную страницу 302 временно
        return redirect("homepage", permanent=True)  # Редирект на главную страницу 301 постоянно
    return HttpResponse(f"<h1>Архив за {year} год</h1>")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Ошибка 404. Страница не найдена</h1>")
