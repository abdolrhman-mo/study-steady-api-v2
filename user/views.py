from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .serializers import RelationshipSerializer, UserSerializer, UserDetailsSerializer

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,  IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()[:50]
    
class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailsSerializer
    queryset = User.objects.all()
    

class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,  # Explicitly define request body
        responses={
            201: openapi.Response("User loggedin successfully"),
            400: openapi.Response("Invalid data"),
        }
    )

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class FollowUserView(APIView):
    """Follow a user"""
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
            if request.user == user_to_follow:
                return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

            request.user.follow(user_to_follow)
            return Response({"message": f"You are now following {user_to_follow.username}."}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class UnfollowUserView(APIView):
    """Unfollow a user"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)

            if request.user.is_following(user_to_unfollow):
                request.user.unfollow(user_to_unfollow)
                return Response({"message": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
            return Response({"error": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class FollowersListView(APIView):
    """Get followers of a user"""
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            followers = user.get_followers()
            serializer = RelationshipSerializer(followers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class FollowingListView(APIView):
    """Get users the current user is following"""
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            following = user.get_following()
            serializer = RelationshipSerializer(following, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class UserFollowStatsView(APIView):
    """Get the number of followers and following of a user"""
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            return Response({
                "followers_count": user.followers_count(),
                "following_count": user.following_count()
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
