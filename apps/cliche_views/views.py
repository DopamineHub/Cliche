from rest_framework import viewsets

from utils.viewsets import (
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
)

from .filters import (
    ClicheViewFilterSet,
    ClicheViewMethodFilterSet,
    ClicheViewMethodScriptFilterSet,
)
from .models import (
    ClicheView,
    ClicheViewMethod,
    ClicheViewMethodScript,
)
from .serializers import (
    ClicheViewSerializer,
    ClicheViewMethodSerializer,
    ClicheViewMethodScriptSerializer,
)


class ClicheViewViewSet(
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
    viewsets.ModelViewSet,
):
    """
    view set of cliche view
    """

    filterset_class = ClicheViewFilterSet
    lookup_field = 'uuid'
    queryset = ClicheView.objects.select_related(
        'app',
    ).prefetch_related(
        'methods',
    ).all()
    serializer_class = ClicheViewSerializer


class ClicheViewMethodViewSet(
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
    viewsets.ModelViewSet,
):
    """
    view set of cliche view method
    """

    filterset_class = ClicheViewMethodFilterSet
    lookup_field = 'uuid'
    queryset = ClicheViewMethod.objects.select_related(
        'view',
        'model',
        'filter_schema',
        'input_schema',
        'output_schema',
    ).all()
    serializer_class = ClicheViewMethodSerializer


class ClicheViewMethodScriptViewSet(
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
    viewsets.ModelViewSet,
):
    """
    view set of cliche view method script
    """

    filterset_class = ClicheViewMethodScriptFilterSet
    lookup_field = 'uuid'
    queryset = ClicheViewMethodScript.objects.select_related(
        'method',
        'method__view',
        'script',
    ).all()
    serializer_class = ClicheViewMethodScriptSerializer
