from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from country.models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def index(request):
    posts = Country.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }
    return render(request, 'country/index.html', context)


def show_continent(request, cat_slug):
    posts = Country.objects.filter(cat__slug=cat_slug)
    if len(posts) == 0:
        raise Http404()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_slug,
    }
    return render(request, 'country/index.html', context)


def show_post(request, post_slug):
    post = get_object_or_404(Country, slug=post_slug)
    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'country/post.html', context)


def about(request):
    context = {
        'menu': menu,
        'title': 'О сайте'
    }
    return render(request, 'country/about.html', context)


def addpage(request):
    return HttpResponse("Добавить статью")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Войти")


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
