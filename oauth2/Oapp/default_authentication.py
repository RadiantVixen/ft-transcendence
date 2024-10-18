from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, User
from django.db import IntegrityError
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_name = request.data.get('user_name')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        language = request.data.get('language')

        if not all([user_name, password, email, first_name, last_name, language]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=user_name).exists():
            return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=user_name,
                email=email,
                password=password
            )

            profile, created = Profile.objects.get_or_create(user=user)
            profile.first_name = first_name
            profile.last_name = last_name
            profile.language = language
            profile.save()


            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully!',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            return Response({"error": "An error occurred while creating the user." + str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
