from django.apps import apps
from rest_framework import serializers

from .models import (
    ClicheModel,
    ClicheModelFieldType,
    ClicheModelField,
)


class ClicheModelSerializer(serializers.ModelSerializer):
    """
    cliche model serializer
    """

    class FieldSerializer(serializers.ModelSerializer):
        id = serializers.ReadOnlyField(
            source='uuid',
        )
        model_foreign = serializers.ReadOnlyField(
            source='model_foreign.uuid',
            default=None,
        )

        class Meta:
            model = ClicheModelField
            ref_name = 'ClicheModel:Field'
            read_only_fields = (
                'id',
                'type',
                'name',
                'attributes',
                'model_foreign',
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
        model = ClicheModel
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
        validated_data.pop('app', None)  # not allowed to change app
        return super().update(instance, validated_data)


class ClicheModelFieldTypeSerializer(serializers.ModelSerializer):
    """
    cliche model field type serializer
    """
    id = serializers.ReadOnlyField(
        source='name',
    )

    class Meta:
        model = ClicheModelFieldType
        read_only_fields = (
            'id',
            'name',
            'description',
            'attributes',
        )
        fields = read_only_fields


class ClicheModelFieldSerializer(serializers.ModelSerializer):
    """
    cliche model field serializer
    """
    id = serializers.ReadOnlyField(
        source='uuid',
    )
    model = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=ClicheModel.objects.all(),
    )
    # for foreign key
    model_foreign = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=ClicheModel.objects.all(),
        required=False,
        default=None,
    )
    type = serializers.SlugRelatedField(
        slug_field='name',
        queryset=ClicheModelFieldType.objects.all(),
        required=True,
    )
    type_attributes = serializers.ReadOnlyField(
        source='type.attributes',
    )

    class Meta:
        model = ClicheModelField
        read_only_fields = (
            'id',
            'uuid',
            'created_time',
            'modified_time',

            'type_attributes',
        )
        fields = (
            'model',
            'model_foreign',
            'type',
            'name',
            'description',
            'attributes',
            *read_only_fields,
        )

    def update(self, instance, validated_data):
        validated_data.pop('model', None)  # not allowed to change model
        return super().update(instance, validated_data)

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.validate()
        return instance
