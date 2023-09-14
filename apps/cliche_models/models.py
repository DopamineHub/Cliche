from uuid import uuid1

from django.db import models

from utils.models.mixins import VersionedModelMixin


class ClicheModel(VersionedModelMixin, models.Model):
    """
    cliche model
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    # owner app
    app = models.ForeignKey(
        'cliche_apps.ClicheApp',
        related_name='models',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    # model name
    name = models.CharField(
        max_length=255,
    )
    # description
    description = models.TextField(
        default='',
        blank=True,
    )
    # attributes
    attributes = models.JSONField(
        blank=True,
        default=dict,
    )

    class Meta:
        unique_together = [
            ('app', 'name'),
        ]

    def __str__(self):
        return f'{str(self.app)}.{self.name}'


class ClicheModelFieldType(models.Model):
    """
    cliche model field type
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


class ClicheModelField(VersionedModelMixin, models.Model):
    """
    cliche model field
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    # owner model
    model = models.ForeignKey(
        ClicheModel,
        related_name='fields',
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    # foreign model when type is ForeignKey
    model_foreign = models.ForeignKey(
        ClicheModel,
        null=True,
        blank=True,
        default=None,
        related_name='foreign_fields',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    # field type
    type = models.ForeignKey(
        ClicheModelFieldType,
        related_name='fields',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    # field name
    name = models.CharField(
        max_length=255,
    )
    # description
    description = models.TextField(
        default='',
        blank=True,
    )
    # attributes
    attributes = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        unique_together = [
            ('model', 'name'),
        ]

    def __str__(self):
        return f'{str(self.model)}:{self.name}'

    def validate(self):
        from rest_framework import exceptions

        if self.type.name == 'ForeignKey':
            if self.model_foreign is None:
                raise exceptions.ValidationError(
                    'foreign key not specified')

            if (
                    (
                        self.model.app_id !=
                        self.model_foreign.app_id
                    )
                    and not self.model.app.is_depending_on(
                        self.model_foreign.app
                    )
            ):
                raise exceptions.ValidationError(
                    'foreign key should be in '
                    'the same app or its dependency')

        else:
            if self.model_foreign is not None:
                raise exceptions.ValidationError(
                    'foreign key should be null')
