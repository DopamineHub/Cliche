from django.contrib import admin

from .models import (
    ClicheSchema,
    ClicheSchemaField,
)


class ClicheSchemaAdmin(admin.ModelAdmin):
    """
    cliche schema admin
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('app')


class ClicheSchemaFieldAdmin(admin.ModelAdmin):
    """
    cliche schema field admin
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('schema', 'schema__app')


admin.site.register(ClicheSchema, ClicheSchemaAdmin)
admin.site.register(ClicheSchemaField, ClicheSchemaFieldAdmin)
