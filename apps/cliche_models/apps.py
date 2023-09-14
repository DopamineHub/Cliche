from django.apps import AppConfig


class ClicheModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cliche_models'
    label = 'cliche_models'

    def ready(self):
        from .signals import on_app_dependency_delete
        assert on_app_dependency_delete
