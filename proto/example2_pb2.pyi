from google.protobuf import descriptor as _descriptor, message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceConfig(_message.Message):
    __slots__ = ("port", "monitoring_url", "service")
    class Service(_message.Message):
        __slots__ = ("timeout_ms",)
        TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
        timeout_ms: int
        def __init__(self, timeout_ms: _Optional[int] = ...) -> None: ...
    PORT_FIELD_NUMBER: _ClassVar[int]
    MONITORING_URL_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    port: int
    monitoring_url: str
    service: ServiceConfig.Service
    def __init__(self, port: _Optional[int] = ..., monitoring_url: _Optional[str] = ..., service: _Optional[_Union[ServiceConfig.Service, _Mapping]] = ...) -> None: ...
