from django.urls import path
from .views import RegisterView, LoginView
from .views import UserListView, UserDetailView, FollowUserView, UnfollowUserView, FollowersListView, FollowingListView, FollowingListStreaksView, UserFollowStatsView, CheckFollowStatusView

urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detials'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # Following & Followers
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('followers/<int:user_id>/', FollowersListView.as_view(), name='get-followers'),
    path('following/<int:user_id>/', FollowingListView.as_view(), name='get-following'),
    path('following/<int:user_id>/streaks/', FollowingListStreaksView.as_view(), name='get-following'),
    path('stats/<int:user_id>/', UserFollowStatsView.as_view(), name='stats'),
    path("check/<int:user_id>/", CheckFollowStatusView.as_view(), name="check-follow-status"),
]
