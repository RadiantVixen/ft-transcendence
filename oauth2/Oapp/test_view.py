
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from .models import Profile, Friendship
from .serializers import ProfileSerializer, UserSerializer, FriendshipSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
import requests

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

class ShowUser(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        if user.is_authenticated:
            if hasattr(user, 'profile'):
                return Response({
                "message": "User authenticated successfully",
                "user_info": {
                    "id" : user.profile.fortytwo_id,
                    "avatar" : user.profile.avatar,
                    "language" : user.profile.language,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
                })
            else:
                return Response({"error": "User profile does not exist"}, status=404)
        else:
            return Response({"error": "user does not exist"}, status=401)

class AllUserInfo(APIView):
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({"error": "Authorization code not provided"}, status=400)

        token_url = 'https://api.intra.42.fr/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.FORTY_TWO_CLIENT_ID,
            'client_secret': settings.FORTY_TWO_CLIENT_SECRET,
            'code': code,
            'redirect_uri': settings.REDIRECT_URI,
        }
        
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get('access_token')
        if access_token:
            # Fetch user info
            user_info_url = 'https://api.intra.42.fr/v2/me'
            headers = {'Authorization': f'Bearer {access_token}'}
            user_response = requests.get(user_info_url, headers=headers)
            user_response.raise_for_status()
            user_data = user_response.json()
            return Response(user_data)


from django.urls import path

urlpatterns = [
    path('listing/', UserListView.as_view(), name='users_list'),
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profile/<int:user_id>/', ShowUser.as_view(), name='profile'),
]

