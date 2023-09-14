from rest_framework import (
    exceptions,
    serializers,
)

from .models import (
    ClicheApp,
    ClicheAppDependency,
)


class ClicheAppSerializer(serializers.ModelSerializer):
    """
    cliche app serializer
    """

    class DependencySerializer(serializers.ModelSerializer):
        """
        dependency serializer
        """
        id = serializers.ReadOnlyField(
            source='dependency.uuid',
        )
        uuid = serializers.ReadOnlyField(
            source='dependency.uuid',
        )
        name = serializers.ReadOnlyField(
            source='dependency.name',
        )

        class Meta:
            model = ClicheAppDependency
            ref_name = 'ClicheApp:Dependency'
            read_only_fields = (
                'id',
                'uuid',
                'name',
            )
            fields = read_only_fields

    id = serializers.ReadOnlyField(
        source='uuid',
    )
    # show all dependencies
    dependencies = DependencySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = ClicheApp
        read_only_fields = (
            'id',
            'uuid',
            'created_time',
            'modified_time',

            'dependencies',
        )
        fields = (
            'name',
            'path',
            *read_only_fields,
        )


class ClicheAppDependencySerializer(serializers.ModelSerializer):
    """
    dependency serializer
    """
    id = serializers.ReadOnlyField(
        source='uuid',
    )
    dependency = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=ClicheApp.objects.all(),
        required=True,
    )
    dependency_name = serializers.ReadOnlyField(
        source='dependency.name',
    )
    dependant = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=ClicheApp.objects.all(),
        required=True,
    )
    dependant_name = serializers.ReadOnlyField(
        source='dependant.name',
    )

    class Meta:
        model = ClicheAppDependency
        read_only_fields = (
            'id',
            'uuid',
            'created_time',
            'modified_time',

            'dependency_name',
            'dependant_name',
        )
        fields = (
            'dependency',
            'dependant',
            *read_only_fields,
        )

    def update(self, instance, validated_data):
        raise exceptions.PermissionDenied(
            'not allowed to modify app dependencies')

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.validate()
        return instance
