from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from country.models import *


# Если форма не связана с моделью
# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label="Название страны", widget=forms.TextInput(attrs={'class': 'form-input'}))
#     # widget - добавление класса для css
#     slug = forms.SlugField(max_length=255, label="URL")
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Описание страны")
#     is_published = forms.BooleanField(label="Публикация", required=False, initial=True)
#     # required - обязательно ли заполнять поле , initial - будет отмечен
#     cat = forms.ModelChoiceField(queryset=Continent.objects.all(), label="Материк", empty_label="Не выбрано")

# Если форма связана с моделью
class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Не выбран"

    class Meta:
        model = Country
        fields = ['title', 'slug', 'content', 'population', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError("Длина превышает 100 символов")
        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Почта:', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля:', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя:', max_length=255)
    email = forms.EmailField(label='Почта:')
    content = forms.CharField(label='Сообщение:', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(label='Капча:')

