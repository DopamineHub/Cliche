from django.apps import apps
from rest_framework import serializers

from .models import (
    ClicheView,
    ClicheViewMethod,
    ClicheViewMethodScript,
)


class ClicheViewSerializer(serializers.ModelSerializer):
    """
    cliche view serializer
    """

    class MethodSerializer(serializers.ModelSerializer):
        id = serializers.ReadOnlyField(
            source='uuid',
        )

        class Meta:
            model = ClicheViewMethod
            ref_name = 'ClicheView:Method'
            read_only_fields = (
                'id',
                'uuid',
                'type',
                'description',
            )
            fields = read_only_fields

    id = serializers.ReadOnlyField(
        source='uuid',
    )
    app = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=apps.get_model('cliche_apps.ClicheApp').objects.all(),
    )
    app_name = serializers.ReadOnlyField(
        source='app.name',
        default='',
    )
    # show all methods
    methods = MethodSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = ClicheView
        read_only_fields = (
            'id',
            'uuid',
            'created_time',
            'modified_time',

            'app_name',
            'methods',
        )
        fields = (
            'app',
            'name',
            'path',
            *read_only_fields,
        )

    def update(self, instance, validated_data):
        validated_data.pop('app', None)  # can not change app
        return super().update(instance, validated_data)


class ClicheViewMethodSerializer(serializers.ModelSerializer):
    """
    cliche view method serializer
    """
    id = serializers.ReadOnlyField(
        source='uuid',
    )
    view = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=ClicheView.objects.all(),
    )
    view_name = serializers.ReadOnlyField(
        source='view.name',
        default=None,
    )
    model = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=apps.get_model(
            'cliche_models.ClicheModel').objects.all(),
        required=False,
        allow_null=True,
        default=None,
    )
    model_name = serializers.ReadOnlyField(
        source='model.name',
        default='',
    )
    filter_schema = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=apps.get_model(
            'cliche_schemas.ClicheSchema'
        ).objects.all(),
        required=False,
        allow_null=True,
        default=None,
    )
    filter_schema_name = serializers.ReadOnlyField(
        source='filter_schema.name',
        default='',
    )
    input_schema = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=apps.get_model(
            'cliche_schemas.ClicheSchema'
        ).objects.all(),
        required=False,
        allow_null=True,
        default=None,
    )
    input_schema_name = serializers.ReadOnlyField(
        source='input_schema.name',
        default='',
    )
    output_schema = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=apps.get_model(
            'cliche_schemas.ClicheSchema'
        ).objects.all(),
        required=False,
        allow_null=True,
        default=None,
    )
    output_schema_name = serializers.ReadOnlyField(
        source='output_schema.name',
        default='',
    )

    class Meta:
        model = ClicheViewMethod
        read_only_fields = (
            'id',
            'uuid',
            'created_time',
            'modified_time',

            'view_name',
            'model_name',
            'filter_schema_name',
            'input_schema_name',
            'output_schema_name',
        )
        fields = (
            'view',
            'type',
            'description',
            'model',
            'filter_schema',
            'input_schema',
            'output_schema',
            *read_only_fields,
        )

    def update(self, instance, validated_data):
        # not allowed to change view and type
        validated_data.pop('view', None)
        validated_data.pop('type', None)
        return super().update(instance, validated_data)


class ClicheViewMethodScriptSerializer(serializers.ModelSerializer):
    """
    cliche view method script serializer
    """
    id = serializers.ReadOnlyField(
        source='uuid',
    )
    method = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=ClicheViewMethod.objects.all(),
    )
    method_name = serializers.ReadOnlyField(
        source='method.name',
        default=None,
    )
    target = serializers.PrimaryKeyRelatedField(
        queryset=apps.get_model(
            'cliche_builders.ClicheBuildTarget').objects.all(),
    )
    script = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=apps.get_model(
            'cliche_scripts.ClicheScript').objects.all(),
    )
    script_name = serializers.ReadOnlyField(
        source='script.name',
        default=None,
    )

    class Meta:
        model = ClicheViewMethodScript
        read_only_fields = (
            'id',
            'uuid',
            'created_time',
            'modified_time',

            'method_name',
            'script_name',
        )
        fields = (
            'method',
            'target',
            'script',
            'arguments',
            *read_only_fields,
        )

    def update(self, instance, validated_data):
        # not allowed to change target and arguments
        validated_data.pop('target', None)
        validated_data.pop('arguments', None)
        return super().update(instance, validated_data)

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.validate()
        return instance
