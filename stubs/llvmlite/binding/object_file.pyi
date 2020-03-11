from . import ffi as ffi
from ctypes import c_ulonglong as c_ulonglong
from typing import Any

class SectionIteratorRef(ffi.ObjectRef):
    def name(self): ...
    def is_text(self): ...
    def size(self): ...
    def address(self): ...
    def data(self): ...
    def is_end(self, object_file: Any): ...
    def next(self) -> None: ...

class ObjectFileRef(ffi.ObjectRef):
    @classmethod
    def from_data(cls, data: Any): ...
    @classmethod
    def from_path(cls, path: Any): ...
    def sections(self) -> None: ...
