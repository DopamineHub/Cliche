from datetime import timedelta
from typing import (
    Generator,
    Optional,
)
from .services import (
    abstractmethod,
    ABCMeta,
    IService,
)


class IMessageQueue(IService, metaclass=ABCMeta):
    """
    interface for message queue instance
    """

    @abstractmethod
    def send(self, msg: bytes):
        """
        send to message queue
        """

    @abstractmethod
    def poll(self) -> Generator[bytes, None, None]:
        """
        poll from message queue
        """


class IMessageQueueService(IService, metaclass=ABCMeta):
    """
    interface for message queue service
    """

    @abstractmethod
    def get_queue(
            self,
            topic: str,
            timeout: Optional[timedelta] = None,
            **kwargs,
    ) -> Optional[IMessageQueue]:
        """
        to get message queue instance
        """
