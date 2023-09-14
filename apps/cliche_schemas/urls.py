from django.urls import path, include
from utils.routers import DefaultRouter

from .views import (
    ClicheSchemaViewSet,
    ClicheSchemaFieldTypeViewSet,
    ClicheSchemaFieldViewSet,
)

app_name = 'cliche_schemas'

router = DefaultRouter()
router.register(
    'schemas.fields.types',
    ClicheSchemaFieldTypeViewSet,
    basename='cliche-schemas-fields-types',
)
router.register(
    'schemas.fields',
    ClicheSchemaFieldViewSet,
    basename='cliche-schemas-fields',
)
router.register(
    'schemas',
    ClicheSchemaViewSet,
    basename='cliche-schemas',
)

urlpatterns = [path('', include(router.urls))]
