from rest_framework import serializers


class UserAuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(style={'input_type': 'password'})