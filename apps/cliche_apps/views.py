from rest_framework import viewsets

from utils.viewsets import (
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
)

from .filters import (
    ClicheAppFilterSet,
    ClicheAppDependencyFilterSet,
)
from .models import (
    ClicheApp,
    ClicheAppDependency,
)
from .serializers import (
    ClicheAppSerializer,
    ClicheAppDependencySerializer,
)


class ClicheAppViewSet(
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
    viewsets.ModelViewSet,
):
    """
    cliche app view set
    """
    filterset_class = ClicheAppFilterSet
    lookup_field = 'uuid'
    queryset = ClicheApp.objects.prefetch_related(
        'dependencies',
        'dependencies__dependency',
    ).all()
    serializer_class = ClicheAppSerializer


class ClicheAppDependencyViewSet(
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
    viewsets.ModelViewSet,
):
    """
    cliche app dependency view set
    """
    filterset_class = ClicheAppDependencyFilterSet
    lookup_field = 'uuid'
    queryset = ClicheAppDependency.objects.select_related(
        'dependency',
        'dependant',
    ).all()
    serializer_class = ClicheAppDependencySerializer
