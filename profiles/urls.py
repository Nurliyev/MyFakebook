from django.urls import path
from .views import UserDetail, UserUpdate, send_friend_request, accept_friend_request, FriendList, delete_friend_request

urlpatterns = [
    path('<int:pk>/', UserDetail.as_view(), name='profile-detail'),
    path('profile-edit/<int:pk>/', UserUpdate.as_view(), name='profile-edit'),
    path('send_friend_request/<int:userID>/', send_friend_request, name='send friend request'),
    path('accept_friend_request/<int:requestID>/', accept_friend_request, name='accept friend request'),
    path('delete_friend_request/<int:deleteID>/', delete_friend_request, name='delete friend request'),
    path('friends/', FriendList.as_view(), name='friend-list'),
]
