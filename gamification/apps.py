from django.apps import AppConfig


class GamificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gamification'

    def ready(self):
        """
        Import signals when the app is ready.

        This ensures that automatic gamification logic is registered
        when Django starts.
        """
        import gamification.signals