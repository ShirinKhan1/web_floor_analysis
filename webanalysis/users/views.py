from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from float.models import *
from django.shortcuts import redirect
from django.db.models import Count

from users.forms import *


class LoginUSer(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('users:profile')
    # def get_success_url(self):
    #     return reverse


# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = LoginUserForm()
#     return render(request, 'login.html', {'form': form})

class RegisterUSer(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)  # Автоматический вход после регистрации
        messages.success(self.request, 'Регистрация прошла успешно. Вы вошли в систему.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Ошибка регистрации. Проверьте введенные данные.')
        return response

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')  # Перенаправление аутентифицированного пользователя
        return super().dispatch(*args, **kwargs)


def profile(request):
    if not request.user.is_authenticated:
        redirect('users:not_auth')
    user_id = request.user.id
    # list_id_link_area = History.objects.filter(user=user_id)
    # list_id_link_area = list_id_link_area.distinct('linkarea_id')
    list_id_link_area = (
        History.objects
        .filter(user=user_id)
        .values('linkarea_id', 'method')  # Выбор поля linkara_id
        .distinct()  # Удаление дубликатов
    )
    methods = list_id_link_area.values('linkarea_id', 'method', 'create_date_dttm')
    print(methods)
    return render(request, 'profile.html', {'methods': methods})


def method(request, method_id):
    if not request.user.is_authenticated:
        redirect('users:not_auth')
    user_id = request.user.id
    # list_id_link_area = (
    #     History.objects
    #     .filter(user=user_id, linkarea_id=method_id)
    #     .values('linkarea_id', 'method')  # Выбор поля linkara_id
    #     .distinct()  # Удаление дубликатов
    # )
    results = Float.objects.raw(
        f"SELECT ff.* FROM float_history fh JOIN float_float ff ON fh.float_id =ff.id WHERE fh.user_id = {user_id} AND fh.linkarea_id = {method_id}")
    columns = results.columns
    print(results.columns)
    value = [x for x in results.query]
    fixed_value = []
    for val in value:
        fixed_value.append(tuple("Пусто" if value is None else value for value in val))

    print(fixed_value)
    return render(request, 'method.html', {'method': method_id, 'results': fixed_value})


def not_authenticated(request):
    return render(request, 'not_auth.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
