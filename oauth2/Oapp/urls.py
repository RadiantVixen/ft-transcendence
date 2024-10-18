from django.urls import path, include
from . import views, default_authentication, test_view, utils, manage_friends
from .utils import FriendsListView, AddFriendView, RemoveFriendView
from .default_authentication import RegisterView
from .manage_users import IsUserLoggedInView, ChangeImage, DeleteImage, ShowUser, ShowProfile, ListUsers, ListProfiles, UserDeleteView, CurrentUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # jwt tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('intra_login/', views.intra_login_view, name='intra_login'),
    path('callback/', views.callback_view.as_view(), name='callback'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    #user management
    path('current_user/', CurrentUser.as_view(), name='current_user'),
    path('is_logged_in/', IsUserLoggedInView.as_view(), name='is_logged_in'),
    path('user/<int:id>/', ShowUser.as_view(), name='user'),
    path('profile/<int:id>/', ShowProfile.as_view(), name='profile'),
    path('users/', ListUsers.as_view(), name='users'),
    path('profiles/', ListProfiles.as_view(), name='profiles'),
    path('delete_user/<int:id>/', UserDeleteView.as_view(), name='delete_user'),
    path('change_avatar/', ChangeImage.as_view(), name='change_avatar'),
    path('delete_avatar/', DeleteImage.as_view(), name='delete_avatar'),

    #2FA
    path('generate-qr/', views.generate_qr_code, name='generate_qr'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),

    #friends
    path('friends/<int:user_id>/', manage_friends.get_friends, name='get_friends'),
    path('friends/send/', manage_friends.send_friend_request, name='send_friend_request'),
    path('friends/accept/', manage_friends.accept_friend_request, name='accept_friend_request'),
    path('friends/reject/', manage_friends.reject_friend_request, name='reject_friend_request'),
    path('friends/unfriend/', manage_friends.delete_friend, name='delete_friend'),
    path('friends/<int:user_id>/pending/', manage_friends.get_pending_friends, name='get_pending_friends'),
    path('friends/block/', manage_friends.block_friend, name='block_friend'),
    path('friends/unblock/', manage_friends.unblock_friend, name='unblock_friend'),

]


