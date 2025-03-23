from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .serializers import RelationshipSerializer, UserSerializer, UserDetailsSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,  IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.authtoken.models import Token

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate Token instead of JWT
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "message": "User created successfully",
                "token": token.key,
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            # Get or create token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User loggedin successfully",
                "token": token.key,
                "user_id": user.id,
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

class CheckFollowStatusView(APIView):
    """Check if the authenticated user is following a given user"""
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user_to_check = User.objects.get(id=user_id)
            is_following = request.user.is_following(user_to_check)  # Using your signals.py function
            return Response({"is_following": is_following}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)