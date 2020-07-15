from typing import cast, Callable

import subprocess
import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int32

program = pt.Program("module")

My_Struct = pt.StructType({"a": pt.Int32_t, "b": pt.Int32_t, "c": pt.Int32_t})
struct_var = pt.Symbol(My_Struct, "struct_var")

# int test_struct_input(struct my_struct x)
program.add_func_decl("test_struct_input", (My_Struct,), pt.Int32_t)

# struct my_struct test_struct_output(int a, int b, int c)
program.add_func_decl(
    "test_struct_output", (pt.Int32_t, pt.Int32_t, pt.Int32_t), My_Struct
)

program.add_func(
    "struct_in_out",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.DefineVar(
                struct_var,
                pt.Call("test_struct_output", [pt.Int32(1), pt.Int32(2), pt.Int32(3)]),
            ),
            # pt.Return(pt.Int32(1)),
            pt.Return(pt.Call("test_struct_input", [pt.Var(struct_var)])),
        ]
    ),
)

program.add_func(
    "struct_set_get_field",
    (),
    pt.Int32_t,
    pt.Block(
        [
            pt.DefineVar(struct_var),
            pt.Assign(
                pt.Var(struct_var),
                pt.SetElement(pt.Var(struct_var), pt.Int32(1), name="a"),
            ),
            pt.Assign(
                pt.Var(struct_var),
                pt.SetElement(pt.Var(struct_var), pt.Int32(2), idx=1),
            ),
            pt.Assign(
                pt.Var(struct_var),
                pt.SetElement(pt.Var(struct_var), pt.Int32(3), name="c"),
            ),
            pt.Return(
                pt.Add(
                    pt.GetElement(pt.Var(struct_var), name="b"),
                    pt.Add(
                        pt.GetElement(pt.Var(struct_var), idx=2),
                        pt.GetElement(pt.Var(struct_var), name="a"),
                    ),
                )
            ),
        ]
    ),
)


class StructsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = program.compile()
        program.load_library("name")

        struct_in_out = self.engine.get_function_address("struct_in_out")
        self.struct_in_out = cast(Callable[[], int], CFUNCTYPE(c_int32)(struct_in_out))

        struct_set_get_field = self.engine.get_function_address("struct_set_get_field")
        self.struct_set_get_field = cast(
            Callable[[], int], CFUNCTYPE(c_int32)(struct_set_get_field)
        )

    def test_struct_in_out(self) -> None:
        self.assertEqual(self.struct_in_out(), 123)

    def test_struct_set_get_field(self) -> None:
        self.assertEqual(self.struct_set_get_field(), 6)
