from django_filters.rest_framework import (
    filters,
    filterset,
)

from .models import (
    ClicheSchema,
    ClicheSchemaField,
)


class ClicheSchemaFilterSet(filterset.FilterSet):
    app = filters.UUIDFilter(
        field_name='app__uuid',
    )
    name_contains = filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = ClicheSchema
        fields = (
            'app',
            'name',
            'name_contains',
        )


class ClicheSchemaFieldFilterSet(filterset.FilterSet):
    schema = filters.UUIDFilter(
        field_name='schema__uuid',
    )
    schema_nested = filters.UUIDFilter(
        field_name='schema_nested__uuid',
    )

    class Meta:
        model = ClicheSchemaField
        fields = (
            'schema',
            'schema_nested',
        )
