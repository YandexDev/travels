from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from .models import Country, Continent
from .utils import DataMixin


class CountryHome(DataMixin, ListView):
    model = Country
    template_name = "country/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Country.objects.filter(is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        # return dict(list(context.items()) + list(c_def.items()))
        return context | c_def  # Соединяем в один словарь


class CountryContinent(DataMixin, ListView):
    model = Country
    template_name = "country/index.html"
    context_object_name = "posts"
    allow_empty = False  # Вызывает 404 ошибку, если спикоу пуст или не найден

    def get_queryset(self):
        return Country.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Continent.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title="Материк - " + str(c.name),
                                      cat_selected=c.pk)
        return context | c_def


class ShowPost(DataMixin, DetailView):
    model = Country
    template_name = 'country/post.html'
    slug_url_kwarg = 'post_slug'  # название слага для url.py, иначе просто - slug
    # pk_url_kwarg = 'post_pk'  # тоже самое по pk, иначе просто - pk
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return context | c_def


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "country/addpage.html"
    success_url = reverse_lazy('homepage')  # перенаправляет на страницу, после отправки формы
    login_url = reverse_lazy('homepage')  # Перенаправляет если пользователь не авторизован
    raise_exception = True  # Если пользователь не аторизован - выбрасывает 403 ошибку - доступ запрещен

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление страны')
        return context | c_def


class About(DataMixin, TemplateView):
    template_name = 'country/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        return context | c_def


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'country/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context | c_def

    def form_valid(self, form):
        """Авторизует пользователя при успешной проверки формы регистрации"""
        user = form.save()
        login(self.request, user)  # Авторизовывает пользователя
        return redirect('homepage')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'country/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return context | c_def
        # return dict(list(context.items()) + list(c_def.items()))

    # def get_success_url(self):
    #     return reverse_lazy('homepage')  # Указал переопределение в settings.py - LOGIN_REDIRECT_URL


def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Ошибка 404. Страница не найдена</h1>")


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'country/contact.html'
    success_url = reverse_lazy('homepage')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return context | c_def

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('homepage')


# @login_required
# def contact(request):
#     contact_list = Country.objects.all()
#     paginator = Paginator(contact_list, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'country/feedback.html', {'page_obj': page_obj})
#
#
# def list_country(request):
#     return HttpResponse("<h1>Страница со списком стран</h1>")
#
#
# def name_country(request, country):
#     if request.GET:  # http://127.0.0.1:8000/country/russia/?name=Russia&type=Cold
#         print(request.GET)  # <QueryDict: {'name': ['Russia'], 'type': ['Cold']}>
#     return HttpResponse(f"<h1>Описание страны {country}</h1>")
#
#
# def archive(request, year):
#     if int(year) < 1986 or int(year) > 2022:
#         # raise Http404()  Выбросит ошибку 404
#         # return redirect("/")  # Редирект на главную страницу 302 временно
#         return redirect("homepage", permanent=True)  # Редирект на главную страницу 301 постоянно
#     return HttpResponse(f"<h1>Архив за {year} год</h1>")


# def about(request):
#     context = {
#         'menu': menu,
#         'title': 'О сайте'
#     }
#     return render(request, 'country/about.html', context)

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





