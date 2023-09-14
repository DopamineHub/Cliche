from uuid import uuid1

from django.db import models

from utils.models.mixins import VersionedModelMixin


class ClicheSchema(VersionedModelMixin, models.Model):
    """
    cliche schema
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    # owner app
    app = models.ForeignKey(
        'cliche_apps.ClicheApp',
        related_name='schemas',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    # name
    name = models.CharField(
        max_length=255,
    )
    # description
    description = models.TextField(
        blank=True,
        default='',
    )
    # attributes
    attributes = models.JSONField(
        default=dict,
    )

    class Meta:
        unique_together = [
            ('app', 'name'),
        ]

    def __str__(self):
        return f'{str(self.app)}.{self.name}'


class ClicheSchemaFieldType(models.Model):
    """
    cliche schema field type
    """

    # name
    name = models.CharField(
        max_length=16,
        primary_key=True,
    )
    # description
    description = models.TextField()
    # attributes
    attributes = models.JSONField(
        default=dict,
        blank=True,
    )

    def __str__(self):
        return self.name


class ClicheSchemaField(VersionedModelMixin, models.Model):
    """
    cliche schema field
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    # owner schema
    schema = models.ForeignKey(
        ClicheSchema,
        related_name='fields',
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    # foreign schema when type is Nested
    schema_nested = models.ForeignKey(
        ClicheSchema,
        null=True,
        default=None,
        related_name='nested_fields',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    # field type
    type = models.ForeignKey(
        ClicheSchemaFieldType,
        related_name='fields',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    # field name
    name = models.CharField(
        max_length=255,
    )
    # field description
    description = models.TextField(
        blank=True,
        default='',
    )
    # attributes
    attributes = models.JSONField(
        default=dict,
    )

    class Meta:
        unique_together = [
            ('schema', 'name'),
        ]

    def __str__(self):
        return f'{str(self.schema)}:{self.name}'

    def validate(self):
        from rest_framework import exceptions

        if self.type.name == 'Nested':
            if self.schema_nested is None:
                raise exceptions.ValidationError(
                    'foreign schema not specified')

            if (
                    self.schema.app_id !=
                    self.schema_nested.app_id
            ):
                raise exceptions.ValidationError(
                    'foreign schema should be in the same app')

        else:
            if self.schema_nested is not None:
                raise exceptions.ValidationError(
                    'foreign schema should be null')
