from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserAuthenticationSerializer
from .models import UserAuthenticationService
from django.contrib.auth import get_user_model


class AuthenticateUserViewSet(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserAuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            auth_service = UserAuthenticationService(username=username, password=password, request=request)
            response_data = auth_service.get_response()

            return Response(response_data, status=status.HTTP_200_OK) if response_data['status'] == 'success' else Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
