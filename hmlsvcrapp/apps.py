from django.apps import AppConfig


class HmlsvcrappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hmlsvcrapp'

    def ready(self):
        import hmlsvcrapp.signals