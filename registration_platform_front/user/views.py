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
                response = requests.post(
                    f'{settings.APP_A_URL}/api/authenticate/',
                    data={'username': username, 'password': password}
                )
                response.raise_for_status()

                print(f"Response status code: {response.status_code}")
                print(f"Response body: {response.json()}")

                data = response.json()

                if data['status'] == 'success':
                    user, created = User.objects.get_or_create(username=username)
                    if user is not None:
                        login(request, user)
                        organization_id = data.get('organization_id')
                        if organization_id:
                            request.session['organization_id'] = organization_id
                        if data.get('is_admin'):
                            user.is_superuser = True
                            user.save()

                        return redirect('/program/')
                    else:
                        messages.error(request, 'Invalid credentials')
                else:
                    messages.error(request, 'Invalid credentials')
            except requests.RequestException as e:
                messages.error(request, f'Authentication service unavailable: {e}')
                print(f"Request exception: {e}")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
