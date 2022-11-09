from django.apps import AppConfig


class MeetmeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meetme_app'

    def ready(self):
        import meetme_app.signals
