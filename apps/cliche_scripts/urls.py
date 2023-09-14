from django.urls import path, include
from utils.routers import DefaultRouter

from .views import (
    ClicheScriptViewSet,
)

app_name = 'cliche_scripts'

router = DefaultRouter()
router.register(
    'scripts',
    ClicheScriptViewSet,
    basename='cliche-scripts',
)

urlpatterns = [path('', include(router.urls))]
