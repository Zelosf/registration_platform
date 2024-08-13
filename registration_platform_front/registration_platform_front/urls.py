"""
URL configuration for registration_platform_front project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from events.views import register, program_list, speaker_detail, edit_program, user_tickets
from user.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('program/', program_list, name='program_list'),
    path('speakers/<int:speaker_id>', speaker_detail, name='speaker_detail'),
    path('api/register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('program/<int:program_id>/edit/', edit_program, name='update_program'),
    path('my-tickets/', user_tickets, name='user_tickets'),
]
