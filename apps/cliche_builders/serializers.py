from rest_framework import serializers

from .models import (
    ClicheBuildTarget,
    ClicheBuilder,
)


class ClicheBuildTargetSerializer(serializers.ModelSerializer):
    """
    cliche build target
    """
    id = serializers.ReadOnlyField(
        source='name',
    )
    requirements = serializers.DictField(
        required=False,
        default={},
    )

    class Meta:
        model = ClicheBuildTarget
        read_only_fields = (
            'id',
            'name',
            'description',
            'requirements',
            'code',
        )
        fields = read_only_fields

    # def update(self, instance, validated_data):
    #     # not allowed to change name
    #     validated_data.pop('name', None)
    #     return super().update(instance, validated_data)


class ClicheBuilderSerializer(serializers.ModelSerializer):
    """
    cliche builder serializer
    """
    id = serializers.ReadOnlyField(
        source='uuid',
    )
    target = serializers.SlugRelatedField(
        slug_field='name',
        queryset=ClicheBuildTarget.objects.all(),
    )
    settings = serializers.DictField(
        required=False,
        default={},
    )
    requirements = serializers.DictField(
        required=False,
        default={},
    )

    class Meta:
        model = ClicheBuilder
        read_only_fields = (
            'id',
            'uuid',
            'created_time',
            'modified_time',
        )
        fields = (
            'name',
            'directory',
            'target',
            'settings',
            'requirements',
            *read_only_fields,
        )

    def create(self, validated_data):
        # update default requirements
        build_target = validated_data.get('target')
        build_requirements = validated_data.get('requirements') or {}
        build_requirements.update(build_target.requirements)
        validated_data['requirements'] = build_requirements
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # do not allow to change target
        validated_data.pop('target', None)
        return super().update(instance, validated_data)
