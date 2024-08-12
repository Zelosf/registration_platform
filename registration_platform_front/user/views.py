from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login
from .forms import LoginForm
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                # Отправка данных на API приложения A
                response = requests.post(
                    f'{settings.APP_A_URL}/api/authenticate/',
                    data={'username': username, 'password': password}
                )
                response.raise_for_status()  # Проверка на HTTP ошибки
                data = response.json()

                if data['status'] == 'success':
                    # Успешная аутентификация
                    user, created = User.objects.get_or_create(username=username)
                    login(request, user)
                    return redirect('/program/')  # Используйте имя маршрута, а не путь к файлу
                else:
                    messages.error(request, 'Invalid credentials')
            except requests.RequestException as e:
                messages.error(request, f'Authentication service unavailable: {e}')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
