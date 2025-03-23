from rest_framework import serializers

class StreakSerializer(serializers.Serializer):
    current_streak = serializers.IntegerField()
    top_streak = serializers.IntegerField()