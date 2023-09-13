from django.conf import settings
from django.db import models


class VersionedCreatedModelMixin(models.Model):
    """
    versioned create model mixin
    """

    # created time
    created_time = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class VersionedModelMixin(VersionedCreatedModelMixin):
    """
    versioned model mixin
    """

    # last modified time
    modified_time = models.DateTimeField(
        auto_now=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class TrackableCreatedModelMixin(models.Model):
    """
    trackable create model mixin
    """

    # created by user
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
        db_constraint=False,
    )

    class Meta:
        abstract = True


class TrackableModelMixin(TrackableCreatedModelMixin):
    """
    trackable model mixin
    """

    # last modified by user
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
        db_constraint=False,
    )

    class Meta:
        abstract = True
