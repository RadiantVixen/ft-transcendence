from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User,  Friend, Profile
from .serializers import UserSerializer, FriendSerializer, ProfileSerializer

@api_view(['GET'])
def get_friends(request, user_id):
    user = get_object_or_404(User, id=user_id)

    friends = Friend.objects.filter(
        (Q(user=user) | Q(friend=user)) & Q(status=Friend.STATUS_ACCEPTED)
    )
    friends_list = []
    for friend in friends:
        if friend.user == user:
            friends_list.append(friend.friend)
        else:
            friends_list.append(friend.user)

    # friends_list = [f.friend if f.user == user else f.user for f in friends]

    serializer = UserSerializer(friends_list, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_pending_friends(request, user_id):
    user = get_object_or_404(User, id=user_id)
    pending_friends = Friend.objects.filter(friend=user, status=Friend.STATUS_PENDING)
    pending_friends_list = [friendship.user for friendship in pending_friends]
    serializer = UserSerializer(pending_friends_list, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def send_friend_request(request):

    user_id = request.data.get('user_id')
    friend_id = request.data.get('friend_id')


    user = get_object_or_404(User, id=user_id)
    friend = get_object_or_404(User, id=friend_id)
    
    # Check if the friendship already exists
    if Friend.objects.filter(
        Q(user=user, friend=friend) | Q(user=friend, friend=user)
    ).exists():
        return Response({'detail': 'Friend request already sent or already friends'}, status=status.HTTP_400_BAD_REQUEST)


    friendship = Friend.objects.create(user=user, friend=friend, status=Friend.STATUS_PENDING)
    serializer = FriendSerializer(friendship)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def accept_friend_request(request):
    user_id = request.data.get('user_id')
    friend_id = request.data.get('friend_id')
    
    friendship = get_object_or_404(Friend, user=friend_id, friend=user_id)

    if friendship.status == Friend.STATUS_ACCEPTED:
        return Response({'detail': 'Friend request already accepted'}, status=status.HTTP_400_BAD_REQUEST)
    
    friendship.status = Friend.STATUS_ACCEPTED
    friendship.save()
    serializer = FriendSerializer(friendship)
    return Response(serializer.data)

@api_view(['DELETE'])
def reject_friend_request(request):
    user_id = request.data.get('user_id')
    friend_id = request.data.get('friend_id')
    
    friendship = get_object_or_404(Friend, user=friend_id, friend=user_id)
    if friendship.status != Friend.STATUS_PENDING:
        return Response({'detail': 'status is not pending'}, status=status.HTTP_400_BAD_REQUEST)
    friendship.delete()
    return Response({'detail':'request rejected successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_friend(request):
    user_id = request.data.get('user_id')
    friend_id = request.data.get('friend_id')
    
    friendship = Friend.objects.filter(
        (Q(user=user_id) & Q(friend=friend_id)) | 
        (Q(user=friend_id) & Q(friend=user_id))
    ).first()

    if not friendship:
        return Response({'detail': 'Friendship not found'}, status=status.HTTP_404_NOT_FOUND)

    friendship.delete()
    return Response({'detail':'friend deleted successfully'},status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def block_friend(request):
    user_id = request.data.get('user_id')
    friend_id = request.data.get('friend_id')
    
    friendship = Friend.objects.filter(
        (Q(user=user_id) & Q(friend=friend_id)) | 
        (Q(user=friend_id) & Q(friend=user_id))
    ).first()

    if friendship.status == Friend.STATUS_BLOCKED:
        return Response({'detail': 'Friend already blocked'}, status=status.HTTP_400_BAD_REQUEST)
    friendship.status = Friend.STATUS_BLOCKED
    friendship.save()
    serializer = FriendSerializer(friendship)
    return Response(serializer.data)

@api_view(['PUT'])
def unblock_friend(request):
    user_id = request.data.get('user_id')
    friend_id = request.data.get('friend_id')
    
    friendship = Friend.objects.filter(
        (Q(user=user_id) & Q(friend=friend_id)) | 
        (Q(user=friend_id) & Q(friend=user_id))
    ).first()
    
    if friendship.status != Friend.STATUS_BLOCKED:
        return Response({'detail': 'Friend not blocked'}, status=status.HTTP_400_BAD_REQUEST)

    friendship.delete()
    return Response({'detail':'friend unblocked successfully'},status=status.HTTP_204_NO_CONTENT)
