import os

from django.apps import apps
from rest_framework import (
    decorators,
    exceptions,
    response,
    viewsets,
)

from utils.viewsets import (
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
)

from .filters import (
    ClicheBuildTargetFilterSet,
    ClicheBuilderFilterSet,
)
from .models import (
    ClicheBuildTarget,
    ClicheBuilder,
)
from .serializers import (
    ClicheBuildTargetSerializer,
    ClicheBuilderSerializer,
)


class ClicheBuildTargetViewSet(
    viewsets.ReadOnlyModelViewSet,
):
    """
    cliche build target view set
    """

    filterset_class = ClicheBuildTargetFilterSet
    queryset = ClicheBuildTarget.objects.all()
    serializer_class = ClicheBuildTargetSerializer


class ClicheBuilderViewSet(
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
    viewsets.ModelViewSet,
):
    """
    cliche builder view set
    """

    filterset_class = ClicheBuilderFilterSet
    lookup_field = 'uuid'
    queryset = ClicheBuilder.objects.all()
    serializer_class = ClicheBuilderSerializer

    @decorators.action(
        methods=['POST'],
        detail=True,
    )
    def build(self, request, *args, **kwargs):
        instance = self.get_object()

        if os.path.exists(instance.directory):
            if not os.path.isdir(instance.directory):
                raise exceptions.ValidationError(
                    'invalid build directory')
        elif not instance.directory:
            raise exceptions.ValidationError(
                'build directory not specified')
        else:
            try:
                # create directory
                os.makedirs(
                    instance.directory, exist_ok=True)
            except FileNotFoundError as e:
                raise exceptions.ValidationError(
                    f'can not create directory: {str(e)}')

        if not instance.target.code:
            raise exceptions.ValidationError(
                'build code not implemented')

        exec_requirements = instance.target.requirements
        exec_requirements.update(instance.requirements)
        exec_vars = {'project': {
            'name': instance.name,
            'directory': instance.directory,
            'apps': list(apps.get_model(
                'cliche_apps.ClicheApp'
            ).objects.all()),
            'scripts': list(apps.get_model(
                'cliche_scripts.ClicheScript'
            ).objects.filter(app__isnull=True).all()),
            'settings': instance.settings,
            'requirements': exec_requirements,
        }}

        # pre processing ------------------------------------
        if instance.code_start:
            try:
                exec(instance.code_start, exec_vars)
            except Exception as e:
                raise exceptions.APIException(
                    f'Failed Before Build: {str(e)}')

        # build target in directory -------------------------
        try:
            exec(instance.target.code, exec_vars)
        except Exception as e:
            raise exceptions.APIException(
                f'Build Failed: {str(e)}')

        # post processing ------------------------------------
        if instance.code_finish:
            try:
                exec(instance.code_finish, exec_vars)
            except Exception as e:
                raise exceptions.APIException(
                    f'Failed After Build: {str(e)}')

        # ----------------------------------------------------
        return response.Response({'error': 'Build Succeed'})
