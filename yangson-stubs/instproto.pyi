from typing import Protocol
from decimal import Decimal

from .instvalue import Value

class StrInstanceNode(Protocol):
    value: str

class BoolInstanceNode(Protocol):
    value: bool

class IntInstanceNode(Protocol):
    value: int

class DecimalInstanceNode(Protocol):
    value: Decimal

class InstanceRouteInstanceNode(Protocol):
    value: InstanceRoute

class EmptyInstanceNode(Protocol):
    value: tuple[None]

class IdentifierInstanceNode(Protocol):
    value: tuple[str, ...]
    #value: tuple[str, str]

class InstanceNodeProtocol(Protocol):
    value: Value

class ArrayInstanceNodeProtocol(Protocol):
    value: ArrayValue
