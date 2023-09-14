from django.apps import AppConfig


class ClicheSchemasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cliche_schemas'
    label = 'cliche_schemas'

    # def ready(self):
    #     from .signals import on_app_dependency_delete
    #     assert on_app_dependency_delete
