from . import instructions as instructions, types as types, values as values
from typing import Any, ContextManager, Optional, Tuple

class IRBuilder:
    debug_metadata: Any = ...
    def __init__(self, block: Optional[Any] = ...) -> None: ...
    @property
    def block(self): ...
    basic_block: Any = ...
    @property
    def function(self): ...
    @property
    def module(self): ...
    def position_before(self, instr: Any) -> None: ...
    def position_after(self, instr: Any) -> None: ...
    def position_at_start(self, block: Any) -> None: ...
    def position_at_end(self, block: Any) -> None: ...
    def append_basic_block(self, name: str = ...) -> values.Block: ...
    def goto_block(self, block: Any) -> None: ...
    def goto_entry_block(self) -> None: ...
    def if_then(self, pred: values.Value, likely: Optional[bool] = ...) -> ContextManager[values.Block]: ...
    def if_else(self, pred: values.Value, likely: Optional[bool] = ...) -> ContextManager[Tuple[ContextManager[values.Block], ContextManager[values.Block]]]: ...
    def shl(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def lshr(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def ashr(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def add(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def fadd(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def sub(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def fsub(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def mul(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def fmul(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def udiv(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def sdiv(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def fdiv(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def urem(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def srem(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def frem(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def or_(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def and_(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def xor(self, lhs: Any, rhs: Any, name: str = ...) -> instructions.Instruction: ...
    def sadd_with_overflow(
        self, lhs: Any, rhs: Any, name: str = ...
    ) -> instructions.Instruction: ...
    def smul_with_overflow(
        self, lhs: Any, rhs: Any, name: str = ...
    ) -> instructions.Instruction: ...
    def ssub_with_overflow(
        self, lhs: Any, rhs: Any, name: str = ...
    ) -> instructions.Instruction: ...
    def uadd_with_overflow(
        self, lhs: Any, rhs: Any, name: str = ...
    ) -> instructions.Instruction: ...
    def umul_with_overflow(
        self, lhs: Any, rhs: Any, name: str = ...
    ) -> instructions.Instruction: ...
    def usub_with_overflow(
        self, lhs: Any, rhs: Any, name: str = ...
    ) -> instructions.Instruction: ...
    def not_(self, value: Any, name: str = ...): ...
    def neg(self, value: Any, name: str = ...): ...
    def icmp_signed(
        self, cmpop: Any, lhs: Any, rhs: Any, name: str = ...
    ) -> instructions.ICMPInstr: ...
    def icmp_unsigned(
        self, cmpop: Any, lhs: Any, rhs: Any, name: str = ...
    ) -> instructions.ICMPInstr: ...
    def fcmp_ordered(
        self, cmpop: Any, lhs: Any, rhs: Any, name: str = ..., flags: Any = ...
    ): ...
    def fcmp_unordered(
        self, cmpop: Any, lhs: Any, rhs: Any, name: str = ..., flags: Any = ...
    ): ...
    def select(self, cond: Any, lhs: Any, rhs: Any, name: str = ...): ...
    def trunc(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def zext(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def sext(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def fptrunc(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def fpext(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def bitcast(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def addrspacecast(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def fptoui(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def uitofp(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def fptosi(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def sitofp(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def ptrtoint(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def inttoptr(self, value: Any, typ: Any, name: str = ...) -> None: ...
    def alloca(self, typ: Any, size: Optional[Any] = ..., name: str = ...) -> instructions.AllocaInstr: ...
    def load(
        self, ptr: Any, name: str = ..., align: Optional[Any] = ...
    ) -> instructions.LoadInstr: ...
    def store(self, value: Any, ptr: Any, align: Optional[Any] = ...) -> instructions.StoreInstr: ...
    def load_atomic(self, ptr: Any, ordering: Any, align: Any, name: str = ...): ...
    def store_atomic(self, value: Any, ptr: Any, ordering: Any, align: Any): ...
    def switch(self, value: Any, default: Any): ...
    def branch(self, target: Any): ...
    def cbranch(self, cond: Any, truebr: Any, falsebr: Any): ...
    def branch_indirect(self, addr: Any): ...
    def ret_void(self) -> instructions.Ret: ...
    def ret(self, value: Any): ...
    def resume(self, landingpad: Any): ...
    def call(
        self,
        fn: Any,
        args: Any,
        name: str = ...,
        cconv: Optional[Any] = ...,
        tail: bool = ...,
        fastmath: Any = ...,
    ) -> instructions.CallInstr: ...
    def asm(
        self,
        ftype: Any,
        asm: Any,
        constraint: Any,
        args: Any,
        side_effect: Any,
        name: str = ...,
    ): ...
    def load_reg(self, reg_type: Any, reg_name: Any, name: str = ...): ...
    def store_reg(self, value: Any, reg_type: Any, reg_name: Any, name: str = ...): ...
    def invoke(
        self,
        fn: Any,
        args: Any,
        normal_to: Any,
        unwind_to: Any,
        name: str = ...,
        cconv: Optional[Any] = ...,
        tail: bool = ...,
    ): ...
    def gep(self, ptr: Any, indices: Any, inbounds: bool = ..., name: str = ...): ...
    def extract_element(self, vector: Any, idx: Any, name: str = ...): ...
    def insert_element(self, vector: Any, value: Any, idx: Any, name: str = ...): ...
    def shuffle_vector(
        self, vector1: Any, vector2: Any, mask: Any, name: str = ...
    ): ...
    def extract_value(self, agg: Any, idx: Any, name: str = ...): ...
    def insert_value(self, agg: Any, value: Any, idx: Any, name: str = ...): ...
    def phi(self, typ: Any, name: str = ...): ...
    def unreachable(self): ...
    def atomic_rmw(
        self, op: Any, ptr: Any, val: Any, ordering: Any, name: str = ...
    ): ...
    def cmpxchg(
        self,
        ptr: Any,
        cmp: Any,
        val: Any,
        ordering: Any,
        failordering: Optional[Any] = ...,
        name: str = ...,
    ): ...
    def landingpad(self, typ: Any, name: str = ..., cleanup: bool = ...): ...
    def assume(self, cond: Any): ...
    def fence(
        self, ordering: Any, targetscope: Optional[Any] = ..., name: str = ...
    ): ...
    def bswap(self, cond: Any) -> None: ...
    def bitreverse(self, cond: Any) -> None: ...
    def ctpop(self, cond: Any) -> None: ...
    def ctlz(self, cond: Any, flag: Any) -> None: ...
    def cttz(self, cond: Any, flag: Any) -> None: ...
    def fma(self, a: Any, b: Any, c: Any) -> None: ...
    def convert_from_fp16(self, a: Any, to: Optional[Any] = ..., name: str = ...): ...
    def convert_to_fp16(self, a: Any) -> None: ...