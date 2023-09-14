from django.contrib import admin

from .models import (
    ClicheModel,
    ClicheModelField,
)


class ClicheModelAdmin(admin.ModelAdmin):
    """
    cliche model admin
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('app')


class ClicheModelFieldAdmin(admin.ModelAdmin):
    """
    cliche model field admin
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('model', 'model__app')


admin.site.register(ClicheModel, ClicheModelAdmin)
admin.site.register(ClicheModelField, ClicheModelFieldAdmin)
