from rest_framework import viewsets

from utils.viewsets import (
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
)

from .filters import (
    ClicheScriptFilterSet,
)
from .models import (
    ClicheScript,
)
from .serializers import (
    ClicheScriptSerializer,
)


class ClicheScriptViewSet(
    ProtectedCreateViewSetMixin,
    ProtectedDestroyViewSetMixin,
    viewsets.ModelViewSet,
):
    """
    view set of cliche script
    """

    filterset_class = ClicheScriptFilterSet
    lookup_field = 'uuid'
    queryset = ClicheScript.objects.all()
    serializer_class = ClicheScriptSerializer
