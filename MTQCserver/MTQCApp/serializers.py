from rest_framework import serializers
from MTQCApp.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'token', 'emailVerified')
