from django_filters.rest_framework import (
    filters,
    filterset,
)

from .models import (
    ClicheModel,
    ClicheModelField,
)


class ClicheModelFilterSet(filterset.FilterSet):
    app = filters.UUIDFilter(
        field_name='app__uuid',
    )
    name_contains = filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = ClicheModel
        fields = (
            'app',
            'name',
            'name_contains',
        )


class ClicheModelFieldFilterSet(filterset.FilterSet):
    model = filters.UUIDFilter(
        field_name='model__uuid',
    )
    model_foreign = filters.UUIDFilter(
        field_name='model_foreign__uuid',
    )

    class Meta:
        model = ClicheModelField
        fields = (
            'model',
            'model_foreign',
        )
