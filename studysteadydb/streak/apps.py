from django.apps import AppConfig


class StreakConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'streak'

    def ready(self):
        import streak.signals
