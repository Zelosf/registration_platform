from .models import UserAuthenticationService
from .serializers import UserAuthenticationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AuthenticateUserViewSet(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserAuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            auth_service = UserAuthenticationService(username=username, password=password, request=request)
            user = auth_service.authenticate_user()
            return auth_service.get_response()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)