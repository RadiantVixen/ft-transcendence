from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Profile, Friendship, User
from .serializers import ProfileSerializer, UserSerializer, FriendshipSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import requests
from .tools import download_image
from django.core.files import File
from django.shortcuts import get_object_or_404


class IsUserLoggedInView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"message": "User is logged in."}, status=status.HTTP_200_OK)
        return Response({"message": "User is not logged in."}, status=status.HTTP_401_UNAUTHORIZED)

class CurrentUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ShowUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = get_object_or_404(User, id=id)

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return Response(user_data, status=status.HTTP_200_OK)


class ShowProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user = get_object_or_404(User, id=id)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListUsers(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ListProfiles(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated] 

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)

            if request.user == user:
                return Response({"error": "You cannot delete yourself!"}, status=status.HTTP_400_BAD_REQUEST)

            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class ChangeImage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        avatar_url = request.data.get('avatar')
        if not avatar_url:
            return Response({"error": "Avatar URL is required."}, status=400)
        profile, created = Profile.objects.get_or_create(user=user)
        image_file = download_image(avatar_url)
        if image_file:
            profile.avatar.save(f"{user.username}.png", image_file, save=True)
            return Response({"success": "Avatar updated successfully."}, status=200)
        return Response({"error": "Failed to download avatar."}, status=400)


class DeleteImage(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        default_image_path = f"{settings.MEDIA_ROOT}/default.png"
        with open(default_image_path, 'rb') as default_image:
            profile.avatar.save(f"{user.username}.png", File(default_image), save=True)

        return Response({"success": "Avatar deleted successfully."}, status=200)

