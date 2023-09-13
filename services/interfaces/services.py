from abc import (
    ABCMeta,
    abstractmethod,
)
from io import (
    TextIOWrapper,
)
from typing import (
    Union,
)


class IService(metaclass=ABCMeta):
    """
    the root interface for service
    """

    @abstractmethod
    def query_service(
            self,
            interface: type,
            name: str = '',
    ) -> 'IService':
        """
        get another service by entry
        """


class IServiceSite(metaclass=ABCMeta):

    @abstractmethod
    def get_service(
            self,
            interface: type,
            name: str = '',
    ) -> IService:
        """
        get service instance by service entry
        raise exception if no service found
        """

    @abstractmethod
    def query_service(
            self,
            interface: type,
            name: str = '',
    ) -> IService:
        """
        query service instance by service entry
        """

    @abstractmethod
    def register_service(
            self,
            interface: type,
            implement: IService,
            name: str = '',
    ) -> IService:
        """
        register service with service entries
        """


class IServiceBuilder(metaclass=ABCMeta):

    @abstractmethod
    def load_json(
            self,
            service_site: IServiceSite,
            file_or_filename: Union[str, TextIOWrapper],
    ):
        """
        register service to service site by reading configuration file
        """

    @abstractmethod
    def save_json(
            self,
            service_site: IServiceSite,
            file_or_filename: Union[str, TextIOWrapper],
    ):
        """
        save service from service site to configuration file
        """

    @abstractmethod
    def load_yaml(
            self,
            service_site: IServiceSite,
            file_or_filename: Union[str, TextIOWrapper],
    ):
        """
        register service to service site by reading configuration file
        """

    @abstractmethod
    def save_yaml(
            self,
            service_site: IServiceSite,
            file_or_filename: Union[str, TextIOWrapper],
    ):
        """
        save service from service site to configuration file
        """
