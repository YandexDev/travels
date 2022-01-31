from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from country.forms import *
from country.models import *

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]


class CountryHome(ListView):
    model = Country
    template_name = "country/index.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = "Главная страница"
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Country.objects.filter(is_published=True)


class CountryContinent(ListView):
    model = Country
    template_name = "country/index.html"
    context_object_name = "posts"
    allow_empty = True

    def get_queryset(self):
        return Country.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Материк - " + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context


class ShowPost(DetailView):
    model = Country
    template_name = 'country/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['post']
        return context


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = "country/addpage.html"
    success_url = reverse_lazy('homepage')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Добавление статьи'
        return context

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('homepage')
#     else:
#         form = AddPostForm()
#     context = {
#         'menu': menu,
#         'form': form,
#         'title': 'Добавление описания страны',
#     }
#     return render(request, 'country/addpage.html', context)

# def index(request):
#     posts = Country.objects.all()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'country/index.html', context)

# def show_continent(request, cat_slug):
#     posts = Country.objects.filter(cat__slug=cat_slug)
#     if len(posts) == 0:
#         raise Http404()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_slug,
#     }
#     return render(request, 'country/index.html', context)



# def show_post(request, post_slug):
#     post = get_object_or_404(Country, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'country/post.html', context)



def about(request):
    context = {
        'menu': menu,
        'title': 'О сайте'
    }
    return render(request, 'country/about.html', context)


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
