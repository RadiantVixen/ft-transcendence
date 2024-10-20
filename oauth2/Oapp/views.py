import requests
from django.shortcuts import render , redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.crypto import get_random_string
from django.urls import reverse
from .models import Profile
from .utils import generate_qr_code, verify_otp
from django.middleware.csrf import CsrfViewMiddleware, get_token
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class callback_view(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({"error": "Authorization code not provided"}, status=400)

        # state = request.query_params.get('state')
        # if not state or state != request.session.get('oauth_state'):
        #     return Response({"error": "Invalid state parameter"}, status=400)

        token_url = 'https://api.intra.42.fr/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.FORTY_TWO_CLIENT_ID,
            'client_secret': settings.FORTY_TWO_CLIENT_SECRET,
            'code': code,
            'redirect_uri': settings.REDIRECT_URI,
        }

        try:
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

                # Authenticate user
                user = authenticate(
                    request,
                    avatar=user_data['image']['link'],
                    language="english",
                    login=user_data['login'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )

                if user:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'message': 'User authenticated successfully',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Authentication failed"}, status=401)
            else:
                return Response({"error": "Access token not found in response"}, status=400)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to obtain access token: {str(e)}"}, status=400)


def intra_login_view(request):
    # state = get_random_string(32)
    # request.session['oauth_state'] = state

    auth_url = (
        f"https://api.intra.42.fr/oauth/authorize"
        f"?client_id={settings.FORTY_TWO_CLIENT_ID}"
        f"&redirect_uri={settings.REDIRECT_URI}"
        f"&response_type=code"
        # f"&state={state}"
        # f"&force_verify=true"
    )

    response = redirect(auth_url)
    # response.delete_cookie('_intra_42_session_production')
    return response

@method_decorator(login_required, name='dispatch')
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})

