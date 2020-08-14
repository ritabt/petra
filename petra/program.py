"""
This file defines Petra programs.
"""

from __future__ import annotations  # necessary to avoid forward declarations
from llvmlite import ir, binding
from typing import Dict, List, Tuple, Optional

from .block import Block
from .codegen import convert_func_type
from .function import Ftypein, Ftypeout, Function
from .statement import Statement
from .symbol import Symbol


class Program(object):
    """
    A Petra program. Petra programs can be codegen'ed to LLVM.
    """


    llvm_initialized: bool = False

    def __init__(self, name: str):
        self.module = ir.Module(name=name)
        self.functypes: Dict[str, Tuple[Ftypein, Ftypeout]] = dict()
        self.funcs: Dict[str, ir.Function] = dict()
        self.llvm_initialized = True
        binding.initialize()
        binding.initialize_native_target()
        binding.initialize_native_asmprinter()
        target = binding.Target.from_default_triple()  
        self.target_machine: binding.TargetMachine = target.create_target_machine()

    def add_func_decl(
        self, 
        name: str, 
        t_in: Ftypein, 
        t_out: Ftypeout,
        attributes: Optional[Tuple[Tuple[str, ...], ...]] = None,
        func_attributes: Optional[Tuple[str, ...]] = None,
    ) -> Program:
        if name in self.functypes:
            raise Exception("Function %s already exists in program." % name)
        self.functypes[name] = (t_in, t_out)
        self.funcs[name] = ir.Function(
            self.module, convert_func_type(t_in, t_out), name
        )
        if attributes is not None:
            for i in range(len(attributes)):
                if attributes[i] is None:
                    continue
                x: ir.Argument = self.funcs[name].args[i]
                for a in attributes[i]:
                    x.add_attribute(a)
        if func_attributes is not None:
            for a in func_attributes:
                if a is not None:
                    self.funcs[name].attributes.add(a) 
        return self

    def add_func(
        self,
        name: str,
        args: Tuple[Symbol, ...],
        t_out: Ftypeout,
        block: Block,
        attributes: Optional[Tuple[Tuple[str, ...], ...]] = None,
        func_attributes: Optional[Tuple[str, ...]] = None,
    ) -> Program:
        if name in self.functypes:
            raise Exception("Function %s already exists in program." % name)
        t_in = tuple(arg.get_type() for arg in args)
        self.functypes[name] = (t_in, t_out)
        self.funcs[name] = ir.Function(
            self.module, convert_func_type(t_in, t_out), name
        )
        func = Function(name, args, t_out, block, self.functypes, attributes)
        if func_attributes is not None:
            func.attributes = func_attributes
        func.codegen(self.module, self.funcs)
        return self

    def to_llvm(self) -> str:
        return str(self.module)

    def save_object(self, filename: str) -> None:
        backing_mod = binding.parse_assembly(self.to_llvm())
        with open(filename, "wb") as f:
            f.write(self.target_machine.emit_object(backing_mod))

    def compile(self) -> binding.ExecutionEngine:
        print(self.to_llvm())
        backing_mod = binding.parse_assembly(self.to_llvm())
        engine = binding.create_mcjit_compiler(backing_mod, self.target_machine)
        engine.finalize_object()
        engine.run_static_constructors()
        return engine

    # def get_target_machine(self) -> binding.TargetMachine:
    #     return self.target_machine

    def load_library(self, filename: str) -> None:
        binding.load_library_permanently(filename)