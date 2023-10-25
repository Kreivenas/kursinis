from django.apps import AppConfig


class PinigaiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pinigai'

    def ready(self):
        from .signals import create_profile, save_profile

class FamilyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'family'

    def ready(self):
        import signals        