from rest_framework import viewsets

from utils.viewsets import (
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
)

from .filters import (
    ClicheModelFilterSet,
    ClicheModelFieldFilterSet,
)
from .models import (
    ClicheModel,
    ClicheModelFieldType,
    ClicheModelField,
)
from .serializers import (
    ClicheModelSerializer,
    ClicheModelFieldTypeSerializer,
    ClicheModelFieldSerializer,
)


class ClicheModelViewSet(
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
    viewsets.ModelViewSet,
):
    """
    cliche model view set
    """

    filterset_class = ClicheModelFilterSet
    lookup_field = 'uuid'
    queryset = ClicheModel.objects.select_related(
        'app',
    ).prefetch_related(
        'fields',
        'fields__model_foreign',
    ).all()
    serializer_class = ClicheModelSerializer


class ClicheModelFieldTypeViewSet(
    viewsets.ReadOnlyModelViewSet,
):
    """
    cliche model field type view set
    """
    queryset = ClicheModelFieldType.objects.all()
    serializer_class = ClicheModelFieldTypeSerializer


class ClicheModelFieldViewSet(
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
    viewsets.ModelViewSet,
):
    """
    cliche model field view set
    """

    filterset_class = ClicheModelFieldFilterSet
    lookup_field = 'uuid'
    queryset = ClicheModelField.objects.select_related(
        'model',
        'model_foreign',
        'type',
    ).all()
    serializer_class = ClicheModelFieldSerializer
