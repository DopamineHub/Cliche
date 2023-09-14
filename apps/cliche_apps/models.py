from uuid import uuid1
from django.db import models

from utils.models.mixins import (
    VersionedModelMixin,
)


class ClicheApp(VersionedModelMixin, models.Model):
    """
    cliche app
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    # name
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    # app path prefix
    path = models.CharField(
        max_length=511,
        blank=True,
    )

    def __str__(self):
        return self.name

    def is_depending_on(self, app, recursive=False):

        def _is_depending_on(_app, _dep_app, _recur):
            dep_apps = getattr(_app, 'dependencies')
            dep_apps = dep_apps.select_related('dependency')
            for dep_app in dep_apps.all():
                if dep_app == _dep_app:
                    return True

                if _recur:
                    _is_depending_on(dep_app, _dep_app, True)

            return False

        return _is_depending_on(self, app, recursive)


class ClicheAppDependency(VersionedModelMixin, models.Model):
    """
    cliche app dependency
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    # dependant app
    dependant = models.ForeignKey(
        ClicheApp,
        related_name='dependencies',
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    # dependency app
    dependency = models.ForeignKey(
        ClicheApp,
        related_name='dependants',
        on_delete=models.PROTECT,
        db_constraint=False,
    )

    class Meta:
        unique_together = [
            ('dependant', 'dependency'),
        ]

    def __str__(self):
        return f'{str(self.dependant)} depends on {str(self.dependency)}'

    def validate(self):
        from rest_framework import exceptions

        if self.dependant == self.dependency:
            raise exceptions.ValidationError('can not depend on self')

        # ensure dependency tree is a DAG

        def _check_dependencies(app_instance, app_ids: list):
            app_id = getattr(app_instance, 'id')
            if app_id in app_ids:
                raise exceptions.ValidationError('incorrect dependencies')

            app_deps_ids = [app_id, *app_ids]
            app_deps = getattr(app_instance, 'dependencies')
            app_deps = app_deps.select_related('dependency')
            for app_dep in app_deps.all():
                _check_dependencies(app_dep.dependency, app_deps_ids)

        _check_dependencies(self.dependency, [])
