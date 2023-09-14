from collections import OrderedDict
from uuid import uuid1

from django.db import models

from utils.models.mixins import VersionedModelMixin


class ClicheView(VersionedModelMixin, models.Model):
    """
    cliche view model
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    # owner app
    app = models.ForeignKey(
        'cliche_apps.ClicheApp',
        related_name='views',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    # name of views
    name = models.CharField(
        max_length=255,
    )
    # description
    description = models.TextField(
        blank=True,
        default='',
    )
    # path
    path = models.CharField(
        max_length=511,
        blank=True,
    )

    class Meta:
        unique_together = [
            ('app', 'name')
        ]

    def __str__(self):
        return f'{str(self.app)}.{self.name}'


class ClicheViewMethod(VersionedModelMixin, models.Model):
    """
    cliche view method model
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    # owner view
    view = models.ForeignKey(
        ClicheView,
        related_name='methods',
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    # type enumeration
    type_enum = OrderedDict([
        ('GET', 'Get Method'),
        ('POST', 'Post Method'),
        ('PUT', 'Put Method'),
        ('PATCH', 'Patch Method'),
        ('DELETE', 'Delete Method'),
        ('OPTION', 'Option Method'),
    ])
    # method type
    type = models.CharField(
        max_length=16,
        choices=list(type_enum.items()),
    )
    # description
    description = models.TextField(
        blank=True,
        default='',
    )
    # model
    model = models.ForeignKey(
        'cliche_models.ClicheModel',
        null=True,
        default=None,
        related_name='+',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    # filter schema
    filter_schema = models.ForeignKey(
        'cliche_schemas.ClicheSchema',
        null=True,
        default=None,
        related_name='+',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    # request schema
    input_schema = models.ForeignKey(
        'cliche_schemas.ClicheSchema',
        null=True,
        default=None,
        related_name='+',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    # response schema
    output_schema = models.ForeignKey(
        'cliche_schemas.ClicheSchema',
        null=True,
        default=None,
        related_name='+',
        on_delete=models.PROTECT,
        db_constraint=False,
    )

    class Meta:
        unique_together = [
            ('view', 'type'),
        ]

    def __str__(self):
        return f'{str(self.view)}|{self.type}'


class ClicheViewMethodScript(VersionedModelMixin, models.Model):
    """
    cliche view method script
    """
    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    # method
    method = models.ForeignKey(
        ClicheViewMethod,
        related_name='scripts',
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    # build target
    target = models.ForeignKey(
        'cliche_builders.ClicheBuildTarget',
        on_delete=models.PROTECT,
        related_name='+',
        db_constraint=False,
    )
    # script
    script = models.ForeignKey(
        'cliche_scripts.ClicheScript',
        related_name='+',
        on_delete=models.PROTECT,
        db_constraint=False,
    )

    class Meta:
        unique_together = [
            ('method', 'target', 'script'),
        ]

    # arguments (should match the parameters of script)
    arguments = frozenset(sorted([
        'request',
        'options',
    ]))

    def __str__(self):
        return f'{str(self.method)}({self.target})'

    def validate(self):
        from rest_framework import exceptions

        if self.target_id != self.script.target_id:
            raise exceptions.ValidationError(
                'script with different target')

        if (
                self.script.app_id is not None and
                self.script.app_id != self.method.view.app_id
        ):
            raise exceptions.ValidationError(
                'script with different target')

        script_arguments = self.arguments
        script_parameters = self.script.parameters

        # if not isinstance(script_arguments, frozenset):
        #     raise exceptions.ValidationError(
        #         'invalid arguments')

        if not isinstance(script_parameters, dict):
            raise exceptions.ValidationError(
                'invalid parameters')

        # check if arguments match script parameters
        for p_name, _ in script_parameters.items():
            if p_name not in script_arguments:
                raise exceptions.ValidationError(
                    'arguments do not match parameters')
