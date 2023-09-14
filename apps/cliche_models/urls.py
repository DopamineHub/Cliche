from django.urls import path, include
from utils.routers import DefaultRouter

from .views import (
    ClicheModelViewSet,
    ClicheModelFieldTypeViewSet,
    ClicheModelFieldViewSet,
)

app_name = 'cliche_models'

router = DefaultRouter()
router.register(
    'models.fields.types',
    ClicheModelFieldTypeViewSet,
    basename='cliche-models-fields-types',
)
router.register(
    'models.fields',
    ClicheModelFieldViewSet,
    basename='cliche-models-fields',
)
router.register(
    'models',
    ClicheModelViewSet,
    basename='cliche-models',
)

urlpatterns = [path('', include(router.urls))]
