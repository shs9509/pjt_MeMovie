from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model

# community model도 받고
# movie model도 받고
# serializer해서 넘겨주면 됨

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','id',)

