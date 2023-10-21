from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'bloggy'

    def ready(self):
        import bloggy.signals
