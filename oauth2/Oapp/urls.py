from django.urls import path, include
from . import views, default_authentication, test_view, utils
from .utils import FriendsListView, AddFriendView, RemoveFriendView
from .default_authentication import RegisterView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('callback/', views.callback_view.as_view(), name='callback'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.login_view, name='login'),
    path('', include('social_django.urls', namespace='social')),
    path('generate-qr/', views.generate_qr_code, name='generate_qr'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('friends/<int:user_id>/', FriendsListView.as_view(), name='friends-list'),
    path('friends/add/', AddFriendView.as_view(), name='add-friend'),
    path('friends/remove/', RemoveFriendView.as_view(), name='remove-friend'),
]


