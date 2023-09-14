from uuid import uuid1

from django.db import models

from utils.models.mixins import (
    VersionedModelMixin,
)


class ClicheBuildTarget(models.Model):
    """
    cliche build target
    """
    # name of build target
    name = models.CharField(
        max_length=32,
        primary_key=True,
    )
    description = models.TextField(
        default='',
        blank=True,
    )
    # requirements
    requirements = models.JSONField(
        default=dict,
    )
    # build code
    code = models.TextField()

    def __str__(self):
        return self.name


class ClicheBuilder(VersionedModelMixin, models.Model):
    """
    cliche builder
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    # name of build
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    # build target
    target = models.ForeignKey(
        ClicheBuildTarget,
        on_delete=models.PROTECT,
        related_name='builders',
        db_constraint=False,
    )
    # settings
    settings = models.JSONField(
        default=dict,
    )
    # requirements
    requirements = models.JSONField(
        default=dict,
    )
    # build directory
    directory = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    # code start
    code_start = models.TextField(
        default='',
        blank=True,
    )
    # code finish
    code_finish = models.TextField(
        default='',
        blank=True,
    )

    def __str__(self):
        return self.name
