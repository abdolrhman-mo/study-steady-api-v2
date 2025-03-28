from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.models import User
from relationship.models import Relationship
from streak.models import Streak
from django.db.models import Max

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserDetailsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RelationshipSerializer(ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Relationship
        fields = ["id", "follower", "following", "created_at"]

class UserWithStreakSerializer(ModelSerializer):
    top_streak = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'top_streak']

    def get_top_streak(self, obj):
        user_streaks = Streak.objects.filter(user=obj.id)
        top_streak = user_streaks.aggregate(Max('number_of_days')).get("number_of_days__max", 0) or 0

        return top_streak

class RelationshipWithStreaksSerializer(ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserWithStreakSerializer(read_only=True)

    class Meta:
        model = Relationship
        fields = ["id", "follower", "following", "created_at"]