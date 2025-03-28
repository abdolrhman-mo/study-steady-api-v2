from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Streak
from django.db.models import Max

from .serializers import StreakSerializer



class StreakView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print("Streak View")
        print("Authenticated User:", request.user)
        # Last Streak
        user_streaks = Streak.objects.filter(user=kwargs.get("user_id"))
        last_streak = user_streaks.last()

        if last_streak:
            current_streak = last_streak.number_of_days

            today = timezone.now().date()
            last_session_date = last_streak.last_session_date.date()
            days_since_last_session = (today - last_session_date).days

            if days_since_last_session > 1:
                current_streak = 0
        else:
            current_streak = 0

        # Top Streak
        """
        Used .get("number_of_days__max", 0) 
        bcz Max function returns a dict instead of a direct integer
        """
        
        top_streak = user_streaks.aggregate(Max('number_of_days')).get("number_of_days__max", 0) or 0
        
        serializer = StreakSerializer({ "current_streak": current_streak, "top_streak": top_streak })
        return Response(serializer.data)