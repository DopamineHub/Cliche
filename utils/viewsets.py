from django.db import IntegrityError
from django.db.models import ProtectedError
from rest_framework import exceptions


class ProtectedCreateViewSetMixin(object):

    def perform_create(self, serializer):
        try:
            serializer.save()

        except IntegrityError as e:
            raise exceptions.PermissionDenied(
                f'data duplicated: {str(e)}')


class ProtectedDestroyViewSetMixin(object):

    def perform_destroy(self, instance):
        try:
            instance.delete()

        except ProtectedError:
            raise exceptions.PermissionDenied(
                'data is referenced and can not be deleted')
