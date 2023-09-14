from django.apps import apps
from rest_framework import serializers

from .models import (
    ClicheSchema,
    ClicheSchemaFieldType,
    ClicheSchemaField,
)


class ClicheSchemaSerializer(serializers.ModelSerializer):
    """
    serializer of cliche schema
    """

    class FieldSerializer(serializers.ModelSerializer):
        id = serializers.ReadOnlyField(
            source='uuid',
        )
        schema_nested = serializers.ReadOnlyField(
            source='schema_nested.uuid',
            default=None,
        )

        class Meta:
            model = ClicheSchemaField
            ref_name = 'ClicheSchema:Field'
            read_only_fields = (
                'id',
                'type',
                'name',
                'attributes',
                'schema_nested',
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
    # show all fields
    fields = FieldSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = ClicheSchema
        read_only_fields = (
            'id',
            'uuid',
            'created_time',
            'modified_time',

            'app_name',
            'fields',
        )
        fields = (
            'app',
            'name',
            'description',
            'attributes',
            *read_only_fields,
        )

    def update(self, instance, validated_data):
        # not allowed to change app
        validated_data.pop('app', None)
        return super().update(instance, validated_data)


class ClicheSchemaFieldTypeSerializer(serializers.ModelSerializer):
    """
    serializer of cliche schema field type
    """

    id = serializers.ReadOnlyField(
        source='name',
    )

    class Meta:
        model = ClicheSchemaFieldType
        read_only_fields = (
            'id',
            'name',
            'description',
            'attributes',
        )
        fields = read_only_fields


class ClicheSchemaFieldSerializer(serializers.ModelSerializer):
    """
    serializer of cliche schema field
    """

    id = serializers.ReadOnlyField(
        source='uuid',
    )
    schema = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=ClicheSchema.objects.all(),
    )
    # for nested schema
    schema_nested = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=ClicheSchema.objects.all(),
        required=False,
        default=None,
    )
    type = serializers.SlugRelatedField(
        slug_field='name',
        queryset=ClicheSchemaFieldType.objects.all(),
        required=True,
    )
    type_attributes = serializers.ReadOnlyField(
        source='type.attributes',
    )

    class Meta:
        model = ClicheSchemaField
        read_only_fields = (
            'id',
            'uuid',
            'created_time',
            'modified_time',

            'type_attributes',
        )
        fields = (
            'schema',
            'schema_nested',
            'type',
            'name',
            'description',
            'attributes',
            *read_only_fields,
        )

    def update(self, instance, validated_data):
        # not allowed to change schema
        validated_data.pop('schema', None)
        return super().update(instance, validated_data)

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.validate()
        return instance
