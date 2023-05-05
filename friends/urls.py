from django.urls import path

from .views import *

urlpatterns = [
    path('users', UserAPIView.as_view()),
    path('users/<str:username>/friends', FriendsAPIView.as_view()),
    path('users/<str:username>/incoming', IncomingRequestsAPIView.as_view()),
    path('users/<str:username>/outgoing', OutgoingRequestsAPIView.as_view()),
    path('requests', RequestsAPIView.as_view()),
    path('friends', FriendCheckingAPIView.as_view()),

]
