from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from django.db import IntegrityError

class RegisterView(APIView):
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
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            profile, created = Profile.objects.get_or_create(user=user)
            profile.language = language
            profile.save()

            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            return Response({"error": "An error occurred while creating the user." + str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
