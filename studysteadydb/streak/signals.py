from django.db.models.signals import post_save
from django.dispatch import receiver
from session.models import Session
from .models import Streak
from django.utils import timezone

@receiver(post_save, sender=Session)
def manipulate_streak(sender, instance, created, **kwargs):
    if created and instance.duration >= 25:
        user = instance.user
        last_streak = Streak.objects.filter(user=user).last()
        
        if not last_streak:
            Streak.objects.create(user=user, number_of_days=1)
        else:
            today = timezone.now().date() # current date
            last_session_date = last_streak.last_session_date.date() # convert datetime to date

            days_since_last_session = (today - last_session_date).days

            if days_since_last_session > 1: # if more than one day passed since the last session
                Streak.objects.create(user=user, number_of_days=1)
            elif days_since_last_session == 1: # if last session was yesterday
                last_streak.number_of_days += 1
                last_streak.save()
            else:
                pass