from django.urls import path, include
from utils.routers import DefaultRouter

from .views import (
    ClicheViewViewSet,
    ClicheViewMethodViewSet,
    ClicheViewMethodScriptViewSet,
)

app_name = 'cliche_views'

router = DefaultRouter()
router.register(
    'views.methods.scripts',
    ClicheViewMethodScriptViewSet,
    basename='cliche-views-methods-scripts',
)
router.register(
    'views.methods',
    ClicheViewMethodViewSet,
    basename='cliche-views-methods',
)
router.register(
    'views',
    ClicheViewViewSet,
    basename='cliche-views',
)

urlpatterns = [path('', include(router.urls))]
