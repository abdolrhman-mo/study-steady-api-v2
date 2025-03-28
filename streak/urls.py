from django.urls import path
from .views import StreakView

app_name = "streak"

urlpatterns = [
    path('<int:user_id>/', StreakView.as_view(), name="index"),
]