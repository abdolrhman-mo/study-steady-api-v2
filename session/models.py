from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - duration: {self.duration} mins, date and time: {self.created_at}"
