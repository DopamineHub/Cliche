from django.contrib import admin

from .models import (
    ClicheApp,
    ClicheAppDependency,
)


class ClicheAppDependencyAdmin(admin.ModelAdmin):
    """
    cliche app dependency admin
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('dependant', 'dependency')


admin.site.register(ClicheApp)
admin.site.register(ClicheAppDependency, ClicheAppDependencyAdmin)
