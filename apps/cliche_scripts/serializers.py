from rest_framework import serializers
from django.apps import apps

from .models import ClicheScript


class ClicheScriptSerializer(serializers.ModelSerializer):
    """
    cliche script serializer
    """

    id = serializers.ReadOnlyField(
        source='uuid',
    )
    target = serializers.PrimaryKeyRelatedField(
        queryset=apps.get_model(
            'cliche_builders.ClicheBuildTarget').objects.all(),
    )
    app = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=apps.get_model(
            'cliche_apps.ClicheApp').objects.all(),
        allow_null=True,
        default=None,
    )
    app_name = serializers.ReadOnlyField(
        source='app.name',
        default='',
    )

    class Meta:
        model = ClicheScript
        read_only_fields = (
            'id',
            'uuid',
            'created_time',
            'modified_time',
            'app_name',
        )
        fields = (
            'target',
            'app',
            'name',
            'description',
            'imports',
            'parameters',
            'code',
            *read_only_fields,
        )

    def update(self, instance, validated_data):
        # not allowed to change target and parameters
        validated_data.pop('target', None)
        validated_data.pop('app', None)
        validated_data.pop('parameters', None)
        return super().update(instance, validated_data)
