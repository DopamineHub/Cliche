import os

from django.conf import settings
from django.utils.functional import LazyObject

from services.utils.services import (
    ServiceSite,
    ServiceBuilder,
)


class DefaultServiceSite(LazyObject):

    def _setup(self):
        filename_default = os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            'settings',
            'services.yml',
        )
        try:
            filename = getattr(
                settings,
                'SERVICES_CONFIG_FILE',
                filename_default,
            )
        except Exception:  # noqa
            filename = filename_default

        service_site = ServiceSite()
        # service_site.ensure_dependencies()

        service_config = ServiceBuilder()
        # service_config.ensure_dependencies()

        service_config.load_yaml(
            service_site, filename)

        self._wrapped = service_site


default_service_site = DefaultServiceSite()
