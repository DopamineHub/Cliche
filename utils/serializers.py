from rest_framework import serializers


# decorators -------------------------------------------------------------
def trackable_create(update=True):
    def _decorator(create_func):
        def _create(self, validated_data):
            request = self.context.get('request')
            user = request and request.user or None
            validated_data['created_by'] = user
            if update:
                validated_data['modified_by'] = user
            return create_func(self, validated_data)

        return _create

    return _decorator


def trackable_update(update=True):
    def _decorator(update_func):
        if not update:
            return update_func

        def _update(self, instance, validated_data):
            request = self.context.get('request')
            user = request and request.user or None
            validated_data['modified_by'] = user
            return update_func(self, instance, validated_data)

        return _update

    return _decorator


def trackable_serializer(update=True):
    def _decorator(serializer_cls):
        assert issubclass(serializer_cls, serializers.Serializer)
        serializer_cls.create = trackable_create(
            update=update)(serializer_cls.create)
        if update:
            serializer_cls.update = trackable_update(
                update=update)(serializer_cls.update)
        return serializer_cls

    return _decorator


# classes ----------------------------------------------------------------
class SimpleSerializer(serializers.Serializer):

    def create(self, validated_data):
        raise AssertionError('not allowed')

    def update(self, instance, validated_data):
        raise AssertionError('not allowed')


class DictSerializer(serializers.Serializer):

    def create(self, validated_data):
        return {**validated_data}

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance


class UserLoginSerializer(DictSerializer):
    username = serializers.CharField(
        required=True,
        write_only=True,
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
    )
    access_token = serializers.CharField(
        read_only=True,
    )


class UserSelfSerializer(DictSerializer):
    username = serializers.CharField(
        read_only=True,
    )
    email = serializers.CharField(
        read_only=True,
    )
    first_name = serializers.CharField(
        read_only=True,
    )
    last_name = serializers.CharField(
        read_only=True,
    )
    is_staff = serializers.BooleanField(
        read_only=True,
    )
    is_active = serializers.BooleanField(
        read_only=True,
    )
    date_joined = serializers.DateTimeField(
        read_only=True,
    )
