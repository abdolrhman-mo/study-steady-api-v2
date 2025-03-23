from django.urls import path
from .views import StreakView

app_name = "streak"

urlpatterns = [
    path("", StreakView.as_view(), name="index"),
]