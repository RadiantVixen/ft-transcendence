from rest_framework import serializers
from .models import Friendship, Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name'] 

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'fortytwo_id', 'avatar', 'language']

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['id', 'user', 'friend', 'created_at']
