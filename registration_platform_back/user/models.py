# from django.contrib.auth import authenticate
# from django.http import JsonResponse
# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
#
# class CustomUser(AbstractUser):
#     bio = models.TextField(blank=True, null=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     organization_id = models.IntegerField(null=True, blank=True)
#
#     def __str__(self):
#         return self.username if self.username else f"User {self.id}"
#
#
# class UserAuthenticationService:
#     def __init__(self, username, password, request):
#         self.username = username
#         self.password = password
#         self.request = request
#
#     def authenticate_user(self):
#         return authenticate(username=self.username, password=self.password)
#
#     def get_response(self):
#         user = self.authenticate_user()
#         if user:
#             organization_id = getattr(user, 'organization_id', None)
#             print(f"Authenticated user: {user}, Organization ID: {organization_id}")
#             return {
#                 'status': 'success',
#                 'organization_id': organization_id,
#                 'is_admin': user.is_superuser
#             }
#         return {
#             'status': 'error',
#             'message': 'Invalid credentials'
#         }

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username if self.username else f"User {self.id}"



class UserAuthenticationService:
    def __init__(self, username, password, request=None):
        self.username = username
        self.password = password
        self.request = request
        self.user = None

    def authenticate_user(self):
        self.user = authenticate(self.request, username=self.username, password=self.password)
        return self.user

    def get_response(self):
        if self.user is not None:
            # Аутентификация успешна
            return JsonResponse({
                'status': 'success',
                'user_id': self.user.id,
                'username': self.user.username,
                'is_admin': self.user.is_superuser,
            })
        else:
            # Аутентификация не удалась
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)