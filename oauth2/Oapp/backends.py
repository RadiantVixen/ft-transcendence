from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Profile

User = get_user_model()

class FortyTwoBackend(BaseBackend):
    def authenticate(self, request, fortytwo_id=None, avatar=None, **kwargs):
        if fortytwo_id is None or avatar is None:
            return None
        try:
            user = User.objects.get(username=kwargs.get('login'))
        except User.DoesNotExist:
            # Create a new user
            try:
                user = User.objects.create_user(
                    username=kwargs.get('login'),
                    email=kwargs.get('email'),
                    first_name=kwargs.get('first_name'),
                    last_name=kwargs.get('last_name')
                )
            except IntegrityError:
                # Handle any potential race condition
                return None
        profile, created = Profile.objects.get_or_create(user=user) 
        profile.fortytwo_id = fortytwo_id
        profile.avatar = avatar
        profile.language = kwargs.get('language')
        profile.save()
        return user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        




# from django.contrib.auth.models import User
# import requests

# class FortyTwoBackend:
#     def authenticate(self, request, access_token=None):
#         response = requests.get('https://api.intra.42.fr/v2/me', headers={
#             'Authorization': f'Bearer {access_token}'
#         })
        
#         if response.status_code != 200:
#             return None

#         user_data = response.json()
#         email = user_data['email']

#         # Check if a user with this email already exists
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             # Create a new user if one doesn't exist
#             user = User.objects.create(
#                 username=user_data['login'],
#                 email=email
#             )
        
#         return user

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None