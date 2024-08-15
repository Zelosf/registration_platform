from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserAuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(style={'input_type': 'password'})


class UserSerializer(serializers.ModelSerializer):
    organization_id = serializers.IntegerField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'organization_id')