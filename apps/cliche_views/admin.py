from django.contrib import admin

from .models import (
    ClicheView,
    ClicheViewMethod,
    ClicheViewMethodScript,
)


class ClicheViewAdmin(admin.ModelAdmin):
    """
    cliche view admin
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('app')


class ClicheViewMethodAdmin(admin.ModelAdmin):
    """
    cliche view method admin
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'view',
            'view__app',
        )


class ClicheViewMethodScriptAdmin(admin.ModelAdmin):
    """
    cliche view method script admin
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'method',
            'method__view',
            'method__view__app',
        )


admin.site.register(
    ClicheView,
    ClicheViewAdmin,
)
admin.site.register(
    ClicheViewMethod,
    ClicheViewMethodAdmin,
)
admin.site.register(
    ClicheViewMethodScript,
    ClicheViewMethodScriptAdmin,
)
