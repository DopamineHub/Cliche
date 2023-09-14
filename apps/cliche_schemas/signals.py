# from django.apps import apps
# from django.dispatch import receiver
# from django.db import models
# from rest_framework import exceptions
#
# from .models import ClicheSchemaField
#
#
# @receiver(
#     models.signals.pre_delete,
#     sender=apps.get_model('cliche_apps.ClicheAppDependency'),
# )
# def on_app_dependency_delete(
#         sender,
#         instance,
#         *args,
#         **kwargs,
# ):
#     qs = ClicheSchemaField.objects.filter(
#         schema__app_id=instance.dependant_id,
#         schema_nested__app_id=instance.dependency_id,
#     )
#     if qs.exists():
#         raise exceptions.PermissionDenied(
#             'can not remove app dependency due to cliche schema fields')
