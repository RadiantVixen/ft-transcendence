import qrcode
import io
import pyotp
from django.http import HttpResponse
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from PIL import Image
from rest_framework import status
from rest_framework.generics import ListAPIView
from .models import Profile, Friendship, User
from .serializers import ProfileSerializer, UserSerializer, FriendshipSerializer

def generate_qr_code(request):
    user = request.user

    # Check if the user is authenticated
    if not user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    # Create a TOTP device for the user
    totp_device, created = TOTPDevice.objects.get_or_create(user=user, name="default")

    # Get the provisioning URI (for Google Authenticator or similar apps)
    provisioning_uri = totp_device.config_url

    # Generate a QR code from the provisioning URI
    qr = qrcode.make(provisioning_uri)

    # Convert the QR code into an image
    buffer = io.BytesIO()
    qr_img = qr.convert("RGB")  # Convert QR code to an RGB image
    qr_img.save(buffer, format="PNG")  # Save the image to the buffer
    buffer.seek(0)

    # Return the QR code as an image
    return HttpResponse(buffer.getvalue(), content_type="image/png")

@api_view(['POST'])
def verify_otp(request):
    user = request.user

    # Check if the user is authenticated
    if not user.is_authenticated:
        return Response({"status": "unauthorized"}, status=401)

    otp_code = request.data.get('otp_code')

    # Find the user's TOTP device
    try:
        totp_device = TOTPDevice.objects.get(user=user, confirmed=True)
        if totp_device.verify_token(otp_code):
            return Response({"status": "verified"}, status=200)
        else:
            return Response({"status": "invalid code"}, status=400)
    except TOTPDevice.DoesNotExist:
        return Response({"status": "no device found"}, status=404)






# path('friends/<int:user_id>/', FriendsListView.as_view(), name='friends-list'),
# path('friends/add/', AddFriendView.as_view(), name='add-friend'),
# path('friends/remove/', RemoveFriendView.as_view(), name='remove-friend'),

class FriendsListView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            friends = Friendship.objects.filter(user=user)
            serializer = FriendshipSerializer(friends, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class AddFriendView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        friend_id = request.data.get('friend_id')
        try:
            user = User.objects.get(id=user_id)
            friend = User.objects.get(id=friend_id)
            # print(friend.username)
            # Check if they are already friends
            if Friendship.objects.filter(user=user, friend=friend).exists():
                return Response({"error": "Already friends"}, status=status.HTTP_400_BAD_REQUEST)
            # Create a new friendship
            friendship = Friendship(user=user, friend=friend)
            friendship.save()
            return Response({"message": "Friend added"}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User or Friend not found"}, status=status.HTTP_404_NOT_FOUND)

class RemoveFriendView(APIView):
    def delete(self, request):
        user_id = request.data.get('user_id')
        friend_id = request.data.get('friend_id')
        try:
            user = User.objects.get(id=user_id)
            friend = User.objects.get(id=friend_id)
            # Check if the friendship exists
            friendship = Friendship.objects.filter(user=user, friend=friend).first()
            if not friendship:
                return Response({"error": "Friendship does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            # Remove friendship
            friendship.delete()
            return Response({"message": "Friend removed"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User or Friend not found"}, status=status.HTTP_404_NOT_FOUND)
