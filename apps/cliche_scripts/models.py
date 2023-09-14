from uuid import uuid1

from django.db import models

from utils.models.mixins import VersionedModelMixin


class ClicheScript(VersionedModelMixin, models.Model):
    """
    cliche script
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    # build target
    target = models.ForeignKey(
        'cliche_builders.ClicheBuildTarget',
        related_name='scripts',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    app = models.ForeignKey(
        'cliche_apps.ClicheApp',
        default=None,
        null=True,
        related_name='scripts',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    # name of script
    name = models.CharField(
        max_length=255,
    )
    # description
    description = models.TextField(
        blank=True,
    )
    # script imports
    imports = models.JSONField(
        default=dict,
    )
    # script parameters
    parameters = models.JSONField(
        default=dict,
    )
    # script code
    code = models.TextField()

    class Meta:
        unique_together = [
            ('target', 'app', 'name'),
        ]
