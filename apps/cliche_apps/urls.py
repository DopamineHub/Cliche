from django.urls import path, include
from utils.routers import DefaultRouter

from .views import (
    ClicheAppViewSet,
    ClicheAppDependencyViewSet,
)

app_name = 'cliche_apps'

router = DefaultRouter()
router.register(
    'apps.dependencies',
    ClicheAppDependencyViewSet,
    basename='cliche-apps-dependencies',
)
router.register(
    'apps',
    ClicheAppViewSet,
    basename='cliche-apps',
)

urlpatterns = [path('', include(router.urls))]
