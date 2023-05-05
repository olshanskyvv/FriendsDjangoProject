from rest_framework import serializers
from .models import User, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class FriendRequestSerializer(serializers.HyperlinkedModelSerializer):
    sender = UserSerializer()
    recipient = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ('sender', 'recipient')


class SentRequestSerializer(serializers.HyperlinkedModelSerializer):
    recipient = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ('recipient',)


class ReceivedRequestSerializer(serializers.HyperlinkedModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ('sender',)
