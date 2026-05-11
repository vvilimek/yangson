from collections import deque
from datetime import datetime
from typing import Protocol, Union, Optional, overload, Literal, Iterator
from decimal import Decimal
import xml.etree.ElementTree as ET

from .instroute import InstanceRoute
from .instvalue import (ArrayValue, InstanceKey, ObjectValue, Value, StructuredValue)
from .typealiases import (InstanceName, JSONPointer, QualName, ScalarValue, RawScalar, RawValue, SchemaRoute, YangIdentifier)
from .schemanode import DataNode
from .schemadata import SchemaData
from .enumerations import ContentType
from .instance import OutputFilter

class InstanceNodeProtocol(Protocol):
    _key: InstanceKey
    schema_node: DataNode
    schema_data: SchemaData
    timestamp: datetime
    value: Value

    def __init__(self, key: InstanceKey, value: Value,
                 parinst: Optional["InstanceNodeProtocol"],
                 schema_node: DataNode, timestamp: datetime) -> None:
        ...

    @property
    def name(self) -> InstanceName: ...
    @property
    def namespace(self) -> Optional[YangIdentifier]: ...
    @property
    def path(self) -> tuple[InstanceKey]: ...
    def __str__(self) -> str: ...
    def __getitem__(self, key: InstanceKey) -> "InstanceNodeProtocol": ...
    def __iter__(self) -> Iterator: ...
    def json_pointer(self) -> JSONPointer: ...
    def instance_route(self) -> "InstanceRoute": ...
    def is_internal(self) -> bool: ...
    @overload
    def put_member(self, name: InstanceName, value: RawValue, raw: Literal[True]) -> "InstanceNodeProtocol": ...
    @overload
    def put_member(self, name: InstanceName, value: Value, raw: Literal[False]) -> "InstanceNodeProtocol": ...
    @overload
    def put_member(self, name: InstanceName, value: Value) -> "InstanceNodeProtocol": ...
    def put_member(self, naem: InstanceName, value: Union[RawValue, Value], raw: bool = False) -> "InstanceNodeProtocol":
        ...
    def delete_item(self, key: InstanceKey) -> "InstanceNodeProtocol": ...
    def look_up(self, raw: bool = False, **keys: Union[RawScalar, ScalarValue]) -> "ArrayEntryProtocol": ...
    def up(self) -> "InstanceNodeProtocol": ...
    def top(self) -> "RootNodeProtocol": ...
    @overload
    def update(self, value: RawValue, raw: Literal[True]) -> "InstanceNodeProtocol": ...
    @overload
    def update(self, value: Value, raw: Literal[False]) -> "InstanceNodeProtocol": ...
    def update(self, value: Union[RawValue, Value], raw: bool = False) -> "InstanceNodeProtocol": ...
    @overload
    def merge(self, value: Value, raw: Literal[False]) -> "InstanceNodeProtocol": ...
    @overload
    def merge(self, value: Value) -> "InstanceNodeProtocol": ...
    @overload
    def merge(self, value: RawValue, raw: Literal[True]) -> "InstanceNodeProtocol": ...
    def merge(self, value: Union[RawValue, Value], raw: bool = False) -> "InstanceNodeProtocol": ...
    def goto(self, iroute: "InstanceRoute") -> "InstanceNodeProtocol": ...
    def peek(self, iroute: "InstanceRoute") -> Optional[Value]: ...

    def add_defaults(self, ctype: Optional[ContentType] = None, tag: bool = False) -> "InstanceNodeProtocol": ...
    def raw_value(self, filter: OutputFilter = OutputFilter()) -> RawValue: ...
    def to_xml(self, filter: OutputFilter = OutputFilter(), elem: Optional[ET.Element] = None) -> ET.Element: ...

class RootNodeProtocol(InstanceNodeProtocol):
    def __init__(self, value: Value, schema_node: "DataNode",
                 schema_data: "SchemaData", timestamp: datetime) -> None:
        ...
class ObjectMember(InstanceNodeProtocol, Protocol):
    siblings: dict[InstanceName, Value]
    def __init__(self, key: InstanceName,
                 siblings: dict[InstanceName, Value],
                 value: Value, parinst: Optional[InstanceNodeProtocol],
                 schema_node: "DataNode", timestamp: datetime) -> None:
        ...
    def sibling(self, name: InstanceName) -> "ObjectMember": ...

class ArrayEntryProtocol(Protocol):
    before: deque
    after: deque

    def __init__(
            self, key: int, before: deque,
            after: deque, value: Value,
            parinst: Optional[InstanceNodeProtocol],
            schema_node: "DataNode", timestamp: Optional[datetime] = None) -> None:
        ...

    def index(self) -> int: ...
    def previous(self) -> "ArrayEntryProtocol": ...
    def next(self) -> "ArrayEntryProtocol": ...

    @overload
    def insert_before(self, value: Value,
                      raw: Literal[False]) -> "ArrayEntryProtocol": ...
    @overload
    def insert_before(self, value: RawValue,
                      raw: Literal[True]) -> "ArrayEntryProtocol": ...

    def insert_before(self, value: Union[RawValue, Value],
                      raw: bool = False) -> "ArrayEntryProtocol": ...
    @overload
    def insert_after(self, value: Value,
                     raw: Literal[False]) -> "ArrayEntryProtocol": ...
    @overload
    def insert_after(self, value: RawValue,
                     raw: Literal[True]) -> "ArrayEntryProtocol": ...

    def insert_after(self, value: Union[RawValue, Value],
                     raw: bool = False) -> "ArrayEntryProtocol": ...


class MemberName:
    name: YangIdentifier
    ns: Optional[YangIdentifier]
    def __init__(self, name: YangIdentifier, ns: Optional[YangIdentifier]) -> None:
        ...

    # TODO

class StrInstanceNode(InstanceNodeProtocol):
    value: str

class BoolInstanceNode(InstanceNodeProtocol):
    value: bool

class IntInstanceNode(InstanceNodeProtocol):
    value: int

class DecimalInstanceNode(InstanceNodeProtocol):
    value: Decimal

class InstanceRouteInstanceNode(InstanceNodeProtocol):
    value: InstanceRoute

class EmptyInstanceNode(InstanceNodeProtocol):
    value: tuple[None]

class IdentityInstanceNode(InstanceNodeProtocol):
    #value: tuple[str, ...]
    value: tuple[str, str]

class ArrayInstanceNode(InstanceNodeProtocol):
    value: list[Any]
