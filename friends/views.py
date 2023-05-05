from rest_framework import generics
from .models import User, FriendRequest
from .serializers import UserSerializer


class UserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

