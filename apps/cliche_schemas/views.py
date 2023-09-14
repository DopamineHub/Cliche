from rest_framework import viewsets

from utils.viewsets import (
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
)

from .filters import (
    ClicheSchemaFilterSet,
    ClicheSchemaFieldFilterSet,
)
from .models import (
    ClicheSchema,
    ClicheSchemaFieldType,
    ClicheSchemaField,
)
from .serializers import (
    ClicheSchemaSerializer,
    ClicheSchemaFieldTypeSerializer,
    ClicheSchemaFieldSerializer,
)


class ClicheSchemaViewSet(
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
    viewsets.ModelViewSet,
):
    """
    cliche schema view set
    """

    filterset_class = ClicheSchemaFilterSet
    lookup_field = 'uuid'
    queryset = ClicheSchema.objects.select_related(
        'app',
    ).prefetch_related(
        'fields',
        'fields__schema_nested',
    ).all()
    serializer_class = ClicheSchemaSerializer


class ClicheSchemaFieldTypeViewSet(
    viewsets.ReadOnlyModelViewSet,
):
    """
    cliche schema type field view set
    """
    queryset = ClicheSchemaFieldType.objects.all()
    serializer_class = ClicheSchemaFieldTypeSerializer


class ClicheSchemaFieldViewSet(
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
    viewsets.ModelViewSet,
):
    """
    cliche schema field view set
    """

    filterset_class = ClicheSchemaFieldFilterSet
    lookup_field = 'uuid'
    queryset = ClicheSchemaField.objects.select_related(
        'schema',
        'schema_nested',
    ).all()
    serializer_class = ClicheSchemaFieldSerializer
