from importlib import import_module
from io import TextIOWrapper
from typing import Dict, Union

from services.interfaces import (
    IService,
    IServiceSite,
    IServiceBuilder,
)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class
    designated by the last name in the path.
    Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = '%s doesn\'t look like a module path' % dotted_path
        raise ImportError(msg)

    module = import_module(module_path)

    try:

        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        raise ImportError(msg)


class _FileLike(object):
    def __init__(self, file_or_filename: Union[str, TextIOWrapper]):
        if isinstance(file_or_filename, str):
            self.file = open(file_or_filename, 'r')
            self.hold = True

        elif isinstance(file_or_filename, TextIOWrapper):
            self.file = file_or_filename
            self.hold = False

        else:
            raise TypeError('invalid file type')

    def __enter__(self) -> TextIOWrapper:
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.hold:
            self.file.close()


class ServiceSite(IServiceSite):
    """
    default implementation of IServiceSite
    """

    def __init__(self):
        self.service_mapping: Dict[type, Dict[str, IService]] = {}

    def get_service(
            self,
            interface: type,
            name: str = '',
    ) -> IService:
        service = self.query_service(interface, name=name)
        if not service:
            raise LookupError('service not found')
        return service

    def query_service(
            self,
            interface: type,
            name: str = '',
    ) -> IService:
        service = self.service_mapping.get(interface)
        return service and service.get(name)

    def register_service(
            self,
            interface: type,
            implement: IService,
            name: str = '',
    ) -> IService:
        if not issubclass(implement.__class__, interface):
            raise ValueError(
                'incorrect implementation for service interface')

        mapping = self.service_mapping.setdefault(interface, {})
        mapping.update({name: implement})
        return implement


class ServiceBuilder(IServiceBuilder):
    """
    default implementation of ServiceBuilder
    """

    @staticmethod
    def load_object(
            service_site: IServiceSite,
            config_object: Union[tuple, list]
    ):
        if not isinstance(config_object, (tuple, list)):
            raise ValueError('invalid service configuration file')

        for config_item in config_object:
            service_class_name = config_item.pop('class', '')
            service_entries_name = config_item.pop('entries', [])
            if not isinstance(service_entries_name, (tuple, list)):
                raise ValueError(
                    'invalid service entries in configuration file')
            try:
                service_class = import_string(service_class_name)
            except ImportError:
                raise ValueError(
                    'invalid service class {}'.format(service_class_name))

            service_instance = service_class(service_site, **config_item)
            for e in service_entries_name:
                if not isinstance(e, dict):
                    raise ValueError(
                        'invalid service entry in configuration file')

                service_name = e.get('name', '')
                service_interface_name = e.get('interface', '')
                try:
                    service_interface = import_string(service_interface_name)
                except ImportError:
                    raise ValueError('invalid service interface {}'.format(
                        service_interface_name))

                service_site.register_service(
                    service_interface, service_instance, name=service_name)

    def load_json(
            self,
            service_site: IServiceSite,
            file_or_filename: Union[str, TextIOWrapper],
    ):
        import json

        with _FileLike(file_or_filename) as file:
            self.load_object(service_site, json.loads(file.read()))

    def save_json(
            self,
            service_site: IServiceSite,
            file_or_filename: Union[str, TextIOWrapper],
    ):
        raise NotImplementedError()

    def load_yaml(
            self,
            service_site: IServiceSite,
            file_or_filename: Union[str, TextIOWrapper],
    ):
        import yaml

        with _FileLike(file_or_filename) as file:
            self.load_object(service_site, yaml.safe_load(file))

    def save_yaml(
            self,
            service_site: IServiceSite,
            file_or_filename: Union[str, TextIOWrapper],
    ):
        raise NotImplementedError()
