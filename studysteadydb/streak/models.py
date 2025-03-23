from django.db import models
from django.contrib.auth.models import User

class Streak(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_days = models.IntegerField()
    last_session_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - streak: {self.number_of_days}, last session date: {self.last_session_date.date()}"