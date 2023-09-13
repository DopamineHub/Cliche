from django.forms import fields
from django_filters.rest_framework import (
    filters,
)


class NullUUIDField(fields.UUIDField):
    def to_python(self, value):
        return None if value == 'null' else super().to_python(value)


class NullUUIDFilter(filters.UUIDFilter):
    field_class = NullUUIDField
