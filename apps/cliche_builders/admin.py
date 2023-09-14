from django.contrib import admin

from .models import (
    ClicheBuildTarget,
    ClicheBuilder,
)

admin.site.register(ClicheBuildTarget)
admin.site.register(ClicheBuilder)
