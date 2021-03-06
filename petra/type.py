"""
This file defines Petra types.
"""

from abc import ABC, abstractmethod
from llvmlite import ir
from typing import Generic, Optional, Tuple, TypeVar, Union, List, Dict

from .validate import ValidateError


class Type(object):
    """
    A type.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def llvm_type(self) -> ir.Type:
        """
        Return the LLVM type of the given type.
        """
        assert False, "unimplemented"


_T = TypeVar("_T")


class ValueType(Type, Generic[_T]):
    def validate(self, value: _T) -> None:
        """
        Validate values of the type.
        """
        assert False, "unimplemented"


class IntType(ValueType[int]):
    """
    An integer type.
    """

    def __init__(self, bits: int):
        super().__init__("Int%d_t" % bits)
        self.bits = bits

    def validate(self, value: int) -> None:
        exp = self.bits - 1
        if not (-(1 << exp) <= value < (1 << exp)):
            raise ValidateError(
                "Int%d_t value not in the range [-2**%d, 2**%d)."
                % (self.bits, exp, exp)
            )

    def llvm_type(self) -> ir.Type:
        return ir.IntType(self.bits)


class FloatType(ValueType[float]):
    """
    A floating point type.
    """

    def __init__(self, bits: int, name: Optional[str] = None):
        if bits not in (32, 64):
            raise ValidateError("Float bits must be 32 or 64")
        super().__init__(name or "Float%d_t" % bits)
        self.bits = bits

    def validate(self, value: float) -> None:
        pass

    def llvm_type(self) -> ir.Type:
        if self.bits == 32:
            return ir.FloatType()
        elif self.bits == 64:
            return ir.DoubleType()
        else:
            assert False


class BoolType(ValueType[bool]):
    """
    A boolean type.
    """

    def __init__(self) -> None:
        super().__init__("Bool_t")

    def validate(self, value: bool) -> None:
        pass

    def llvm_type(self) -> ir.Type:
        return ir.IntType(1)


class VoidType(Type):
    """
    A void type.
    """

    def __init__(self) -> None:
        super().__init__("Void_t")

    def validate(self, value: None) -> None:
        pass

    def llvm_type(self) -> ir.Type:
        # return ir.VoidType()
        return ir.IntType(8)


# equality to ckeck if the types are the same __eq__
class PointerType(Type):
    """
    A pointer type.
    """

    def __init__(self, pointee: Type) -> None:
        super().__init__("PointerType(%s)" % pointee)
        self.pointee = pointee

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PointerType):
            return False
        return (self.pointee == other.pointee)

    def llvm_type(self) -> ir.Type:
        return ir.PointerType(self.pointee.llvm_type())


class StructType(Type):
    """
    A struct type.
    """

    def __init__(self, elements: Dict[str, Type]) -> None:
        super().__init__("StructType(%s)" % elements)
        self.elements = tuple(elements.values())
        llvm_elements = [t.llvm_type() for t in elements.values()]
        self.struct_type = ir.LiteralStructType(llvm_elements)
        self.name_to_index: Dict[str, int] = {}
        for i, name in enumerate(elements.keys()):
            self.name_to_index[name] = i

    def llvm_type(self) -> ir.Type:
        return self.struct_type


class ArrayType(Type):
    """
    An array type.
    """

    def __init__(self, element: Type, length: int) -> None:
        super().__init__("ArrayType(%s, %s)" % (element, length))
        self.element = element
        self.length = length
        self.array_type = ir.ArrayType(self.element.llvm_type(), self.length)

    def llvm_type(self) -> ir.Type:
        return self.array_type


# Type aliases for functions.
Ftypein = Tuple[Type, ...]
Ftypeout = Union[Tuple[()], Type]

Int8_t = IntType(8)
Int16_t = IntType(16)
Int32_t = IntType(32)
Int64_t = IntType(64)

Float32_t = FloatType(32)
Float64_t = FloatType(64)

Bool_t = BoolType()
Void_t = VoidType()