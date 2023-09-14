from django.urls import path, include
from utils.routers import DefaultRouter

from .views import (
    ClicheBuildTargetViewSet,
    ClicheBuilderViewSet,
)

app_name = 'cliche_builders'

router = DefaultRouter()
router.register(
    'builders.targets',
    ClicheBuildTargetViewSet,
    basename='cliche-builders-targets',
)
router.register(
    'builders',
    ClicheBuilderViewSet,
    basename='cliche-builders',
)

urlpatterns = [path('', include(router.urls))]
