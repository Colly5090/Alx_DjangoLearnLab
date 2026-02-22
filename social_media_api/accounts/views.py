from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({'user': serializer.data, 'token': token.key})
        
        return Response(serializer.errors, status=400)
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'token': serializer.validated_data['token']})
        
        return Response(serializer.errors, status=400)
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    """
    User ViewSet with follow/unfollow functionality.

    Endpoints:
    - GET /users/           : List all users
    - GET /users/{id}/      : Retrieve user details
    - POST /users/{id}/follow/   : Follow a user
    - POST /users/{id}/unfollow/ : Unfollow a user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='follow')
    def follow_user(self, request, pk=None):
        """
        Follow a user by ID.
        """
        user_to_follow = get_object_or_404(User, pk=pk)
        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.following.add(user_to_follow)
        return Response(
            {"detail": f"You are now following {user_to_follow.username}"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], url_path='unfollow')
    def unfollow_user(self, request, pk=None):
        """
        Unfollow a user by ID.
        """
        user_to_unfollow = get_object_or_404(User, pk=pk)
        if user_to_unfollow == request.user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.following.remove(user_to_unfollow)
        return Response(
            {"detail": f"You have unfollowed {user_to_unfollow.username}"},
            status=status.HTTP_200_OK
        )
    
    def create(self, request, *args, **kwargs):
        # Disable creating users via /users/
        return Response(
            {"detail": "You cannot create a user from this endpoint. Use /register/"},
            status=status.HTTP_403_FORBIDDEN
        )