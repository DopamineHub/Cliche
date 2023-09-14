from django_filters.rest_framework import (
    filters,
    filterset,
)

from .models import (
    ClicheView,
    ClicheViewMethod,
    ClicheViewMethodScript,
)


class ClicheViewFilterSet(filterset.FilterSet):
    app = filters.UUIDFilter(
        field_name='app__uuid',
    )
    name_contains = filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = ClicheView
        fields = (
            'app',
            'name',
            'name_contains',
        )


class ClicheViewMethodFilterSet(filterset.FilterSet):
    view = filters.UUIDFilter(
        field_name='view__uuid',
    )

    class Meta:
        model = ClicheViewMethod
        fields = (
            'view',
        )


class ClicheViewMethodScriptFilterSet(filterset.FilterSet):
    method = filters.UUIDFilter(
        field_name='method__uuid',
    )
    script = filters.UUIDFilter(
        field_name='script__uuid',
    )

    class Meta:
        model = ClicheViewMethodScript
        fields = (
            'method',
            'target',
            'script',
        )
