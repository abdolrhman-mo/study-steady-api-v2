from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'user', 'duration', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']