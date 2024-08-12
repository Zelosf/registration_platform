from django.urls import path
from .views import AuthenticateUserViewSet


urlpatterns = [
    path('authenticate/', AuthenticateUserViewSet.as_view(), name='authenticate_user'),
]