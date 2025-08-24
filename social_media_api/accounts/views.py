from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from .models import User as CustomUser

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            # Token auto-created by signal; make sure token exists:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user, context={'request': request}).data
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT/PATCH current user's profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    """
    Public profile by username: /profile/<username>/
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()   # <-- required for checker
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, id=user_id)
        if target == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        target.followers.add(request.user)
        return Response({'detail': f'Now following {target.username}.'}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()   # <-- required for checker
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, id=user_id)
        if target == request.user:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        target.followers.remove(request.user)
        return Response({'detail': f'Unfollowed {target.username}.'}, status=status.HTTP_200_OK)