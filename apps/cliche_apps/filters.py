from django_filters.rest_framework import (
    filters,
    filterset,
)

from .models import (
    ClicheApp,
    ClicheAppDependency,
)


class ClicheAppFilterSet(filterset.FilterSet):
    name_contains = filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = ClicheApp
        fields = (
            'name',
            'name_contains',
        )


class ClicheAppDependencyFilterSet(filterset.FilterSet):
    dependency = filters.UUIDFilter(
        field_name='dependency__uuid',
    )
    dependant = filters.UUIDFilter(
        field_name='dependant__uuid',
    )

    class Meta:
        model = ClicheAppDependency
        fields = (
            'dependency',
            'dependant',
        )
