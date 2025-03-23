from django.urls import path
from .views import RegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserListView, UserDetailView, FollowUserView, UnfollowUserView, FollowersListView, FollowingListView, UserFollowStatsView

urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detials'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Following & Followers
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('followers/<int:user_id>/', FollowersListView.as_view(), name='get-followers'),
    path('following/<int:user_id>/', FollowingListView.as_view(), name='get-following'),
    path('stats/<int:user_id>/', UserFollowStatsView.as_view(), name='stats'),
]
