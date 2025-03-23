from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Relationship(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate follow relationships

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"