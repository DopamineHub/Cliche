from typing import (
    Any,
    Optional,
    List,
    Type,
    TypeVar,
    Union,
)
from services.interfaces import IService

_Int = TypeVar('_Int')  # interface class
_Imp = TypeVar('_Imp')  # implement class


def dynamic_cast(
        instance: Any,
        instance_type: Type[_Int],
) -> Optional[_Int]:
    return (
        instance if
        isinstance(instance, instance_type) else
        None
    )


def implements(
        interfaces: Union[Type[_Int], List[Type[_Int]]]
):
    if issubclass(interfaces, IService):
        interfaces = [interfaces]
    else:
        assert isinstance(interfaces, list)
        for i in interfaces:
            assert issubclass(i, IService)

    def _wrapper(cls: Type[_Imp]):

        class _Wrapper(cls, *interfaces):

            def query_service(
                    self,
                    interface: type,
                    name: str = '',
            ):
                if interface in interfaces:
                    return self
                return None

        return _Wrapper

    return _wrapper
