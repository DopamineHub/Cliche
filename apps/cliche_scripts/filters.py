from django_filters.rest_framework import (
    filters,
    filterset,
)

from .models import (
    ClicheScript,
)


class ClicheScriptFilterSet(filterset.FilterSet):
    app = filters.UUIDFilter(
        field_name='app__uuid',
    )
    name_contains = filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = ClicheScript
        fields = (
            'target',
            'app',
            'name',
            'name_contains',
        )
