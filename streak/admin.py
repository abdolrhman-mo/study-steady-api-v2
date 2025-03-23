from django.contrib import admin
from .models import Streak

@admin.register(Streak)
class StreakAdmin(admin.ModelAdmin):
    list_display = ('user', 'number_of_days', 'last_session_date')