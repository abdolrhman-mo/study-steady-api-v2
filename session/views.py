from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Session

from .serializers import SessionSerializer


class SessionView(ListCreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Session.objects.filter(user=self.request.user)[:50]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


""" 
IF WE WANT TO CHANGE THESE VIEWS TO API VIEWS 
WE'LL NEED TO CHANGE THE RENDERED RESPONCE
FROM HTML --TO-> JSON
"""