from django.apps import AppConfig


class UserConfig(AppConfig):
    name = "constancy_brokers.apps.user"

    def ready(self):
        from . import signals
