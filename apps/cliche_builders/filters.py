from django_filters.rest_framework import (
    filters,
    filterset,
)

from .models import (
    ClicheBuildTarget,
    ClicheBuilder,
)


class ClicheBuildTargetFilterSet(filterset.FilterSet):
    name_contains = filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = ClicheBuildTarget
        fields = (
            'name',
            'name_contains',
        )


class ClicheBuilderFilterSet(filterset.FilterSet):
    name_contains = filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = ClicheBuilder
        fields = (
            'name',
            'name_contains',
            'target',
        )
