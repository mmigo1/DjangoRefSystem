from rest_framework import serializers
from .models import CustomUser, Profile


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = CustomUser.objects.create(phone=validated_data['phone'])
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['phone']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['recommended_by','user']
