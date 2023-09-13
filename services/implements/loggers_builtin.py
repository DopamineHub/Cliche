from logging import (
    getLogger,
    Logger as LoggerBuiltin,
)
from traceback import format_exc
from typing import Dict, Optional

from services.interfaces import IServiceSite
from services.interfaces.loggers import ILogger
from services.utils import implements


@implements(ILogger)
class Logger(object):
    """
    builtin logger
    """

    def __init__(self, service_site: IServiceSite, **kwargs):
        print('create builtin logger service')
        self.loggers: Dict[str, LoggerBuiltin] = {}

    def get_logger(self, topic: str):
        logger = self.loggers.get(topic)
        if not logger:
            logger = getLogger(topic)
            self.loggers[topic] = logger
        return logger

    def info(
            self,
            topic: str,
            msg: Optional[str] = None,
            attrs: Optional[dict] = None,
            exc: Optional[Exception] = None,
    ):
        from django.conf import settings
        if settings.DEBUG:
            print(msg or format_exc())
        else:
            self.get_logger(topic).info(msg or format_exc())

    def warning(
            self,
            topic: str,
            msg: Optional[str] = None,
            attrs: Optional[dict] = None,
            exc: Optional[Exception] = None,
    ):
        self.get_logger(topic).warning(msg or format_exc())

    def error(
            self,
            topic: str,
            msg: Optional[str] = None,
            attrs: Optional[dict] = None,
            exc: Optional[Exception] = None,
    ):
        self.get_logger(topic).error(msg or format_exc())
