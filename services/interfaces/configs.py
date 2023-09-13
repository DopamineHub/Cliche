from typing import Optional
from .services import (
    abstractmethod,
    ABCMeta,
    IService,
)


class IConfig(IService, metaclass=ABCMeta):
    """
    config instance
    """

    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        """
        get value by key
        """


class IConfigService(IService, metaclass=ABCMeta):
    """
    config service
    """

    @abstractmethod
    def get_config(self, name: str) -> IConfig:
        """
        get config by name
        """
