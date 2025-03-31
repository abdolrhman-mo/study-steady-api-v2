from django.utils import timezone
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Session

from .serializers import SessionSerializer


class SessionView(ListCreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Session.objects.filter(user=self.request.user).order_by('-created_at')[:50]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Filter today's sessions
        today = timezone.now().date()
        today_sessions = [session for session in queryset if session.created_at.date() == today]
        print(today_sessions)

        # Serialize today's sessions
        today_sessions_serializer = self.get_serializer(today_sessions, many=True)

        # Today total minutes
        today_total = sum(session.duration for session in today_sessions)

        return Response({
            "sessions": serializer.data,
            "today_sessions": today_sessions_serializer.data,
            "today_total": today_total,
        })


""" 
IF WE WANT TO CHANGE THESE VIEWS TO API VIEWS 
WE'LL NEED TO CHANGE THE RENDERED RESPONCE
FROM HTML --TO-> JSON
"""