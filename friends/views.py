from django.db.models import Q, Model
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer, SentRequestSerializer, ReceivedRequestSerializer


class UserAPIView(ListCreateAPIView):
    """Getting list of users and adding new users"""
    queryset = User.objects.all().order_by('id', 'username')
    serializer_class = UserSerializer


class RequestsAPIView(ListAPIView):
    """Getting list of friend requests"""
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer


class IncomingRequestsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """Getting list of incoming friend requests"""
        username = kwargs.get('username', None)
        if not username:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = User.objects.get(username=username)
        except Model.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        requests = FriendRequest.objects.all().filter(recipient=instance)
        serializer = ReceivedRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Answering to incoming friends requests"""
        username = kwargs.get('username', None)
        answer = request.data.get('answer', None)
        if not username or not answer:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            recipient = User.objects.get(username=username)
            sender = User.objects.get(username=request.data['username'])
            friend_request = FriendRequest.objects.get(Q(sender=sender) & Q(recipient=recipient))
        except Model.DoesNotExist:
            return Response({'error': 'user or friend request not found'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.delete()
        if answer:
            recipient.friends.add(sender)
            return Response({'response': f'friend {sender.username} added'})
        else:
            return Response({'response': f'request from {sender.username} was declined'})


class OutgoingRequestsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """Getting list of outgoing friend requests"""
        username = kwargs.get('username', None)
        if not username:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = User.objects.get(username=username)
        except Model.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        requests = FriendRequest.objects.all().filter(sender=instance)
        serializer = SentRequestSerializer(requests, many=True)
        return Response(serializer.data)


class FriendsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """Getting list of friends"""
        username = kwargs.get('username', None)
        if not username:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = User.objects.get(username=username)
        except Model.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        friends = instance.friends.all()
        if friends:
            return Response(UserSerializer(friends, many=True).data)
        else:
            return Response({'error': 'friends not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        """Creating friend request"""
        username = kwargs.get('username', None)
        if not username:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sender = User.objects.get(username=username)
            recipient = User.objects.get(username=request.data['username'])
        except Model.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        if sender == recipient:
            return Response({'error': "you can't send a request to yourself"}, status=status.HTTP_400_BAD_REQUEST)
        if recipient in sender.friends.all():
            return Response({'error': f'{recipient.username} is already your friend'}, status=status.HTTP_400_BAD_REQUEST)
        back_friend_request = FriendRequest.objects.filter(sender=recipient, recipient=sender)
        if back_friend_request:
            sender.friends.add(recipient)
            back_friend_request.delete()
            return Response({'response': f'User {recipient.username} has already sent request to you. ' +
                                         f'Now you are friends'})
        if FriendRequest.objects.filter(sender=sender, recipient=recipient):
            return Response({'response': f'you have already sent request to {recipient.username}'},
                            status=status.HTTP_400_BAD_REQUEST)
        friend_request = FriendRequest.objects.create(sender=sender, recipient=recipient)
        return Response(FriendRequestSerializer(friend_request).data)

    def delete(self, request, *args, **kwargs):
        """Deleting friend"""
        username = kwargs.get('username', None)
        if not username:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            friend = user.friends.get(username=request.data['username'])
        except Model.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        user.friends.remove(friend)
        return Response({'response': f'friend {friend.username} was deleted'})


class FriendCheckingAPIView(APIView):
    def get(self, request):
        """Check if two users are friends"""
        username1 = request.data.get('username1', None)
        username2 = request.data.get('username2', None)
        if not username1 or not username2:
            return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user1 = User.objects.get(username=username1)
            user2 = User.objects.get(username=username2)
            outgoing = FriendRequest.objects.filter(Q(sender=user1) & Q(recipient=user2))
            incoming = FriendRequest.objects.filter(Q(sender=user2) & Q(recipient=user1))
        except Model.DoesNotExist:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        if user1 in user2.friends.all():
            return Response({'response': 'you are friends'})
        elif outgoing:
            return Response({'response': f'{user1.username} have outgoing request to {user2.username}'})
        elif incoming:
            return Response({'response': f'{user1.username} have incoming request from {user2.username}'})
        else:
            return Response({'response': 'you are not friends and there are no friend requests'})
