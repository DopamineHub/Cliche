from typing import (
    Optional,
)
from .services import (
    abstractmethod,
    ABCMeta,
    IService,
)


class ILogger(IService, metaclass=ABCMeta):
    """
    interface for logger
    """

    @abstractmethod
    def info(
            self,
            topic: str,
            msg: Optional[str] = None,
            attrs: Optional[dict] = None,
            exc: Optional[Exception] = None,
    ):
        """
        log info
        """

    @abstractmethod
    def warning(
            self,
            topic: str,
            msg: Optional[str] = None,
            attrs: Optional[dict] = None,
            exc: Optional[Exception] = None,
    ):
        """
        log warning
        """

    @abstractmethod
    def error(
            self,
            topic: str,
            msg: Optional[str] = None,
            attrs: Optional[dict] = None,
            exc: Optional[Exception] = None,
    ):
        """
        log error
        """
