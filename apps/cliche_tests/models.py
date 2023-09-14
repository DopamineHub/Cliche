from uuid import uuid1

from django.db import models

from utils.models.mixins import VersionedModelMixin


class ClicheTest(VersionedModelMixin, models.Model):
    """
    cliche test model
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuid1,
    )
    # owner app
    app = models.ForeignKey(
        'cliche_apps.ClicheApp',
        related_name='tests',
        on_delete=models.PROTECT,
        db_constraint=False,
    )
