from typing import cast, Callable

import subprocess
import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int32

program = pt.Program("module")

# Global variables
LEGION_MAX_DIM = 2
MAX_DOMAIN_DIM = 2 * LEGION_MAX_DIM
DIM = 1

# Define types:
legion_region_tree_id_t = pt.Int64_t
legion_index_partition_id_t = pt.Int64_t
legion_index_tree_id_t = pt.Int64_t
legion_type_tag_t = pt.Int64_t
legion_field_space_id_t = pt.Int64_t
coord_t = pt.Int64_t
legion_index_space_id_t = pt.Int64_t
# is realm an int
realm_id_t = pt.Int64_t

# how can I define void*
legion_runtime_t = pt.StructType({"impl": pt.PointerType(pt.Int64_t)})

legion_index_partition_t = pt.StructType(
    {
        "id": legion_index_partition_id_t,
        "tid": legion_index_tree_id_t,
        "type_tag": legion_type_tag_t,
    }
)

legion_field_space_t = pt.StructType({"id": legion_field_space_id_t})

legion_logical_partition_t = pt.StructType(
    {
        "tree_id": legion_region_tree_id_t,
        "index_partition": legion_index_partition_t,
        "field_space": legion_field_space_t,
    }
)

legion_domain_point_t = pt.StructType(
    {"dim": pt.Int64_t, "point_data": pt.ArrayType(coord_t, LEGION_MAX_DIM)}
)

legion_domain_t = pt.StructType({"is_id": realm_id_t, "dim": pt.Int64_t})

legion_point_1d_t = pt.StructType({"x": pt.ArrayType(coord_t, DIM)})

legion_index_space_t = pt.StructType(
    {
        "id": legion_index_space_id_t,
        "tid": legion_index_tree_id_t,
        "type_tag": legion_type_tag_t,
    }
)

legion_logical_region_t = pt.StructType(
    {
        "tree_id": legion_region_tree_id_t,
        "index_space": legion_index_space_t,
        "field_space": legion_field_space_t,
    }
)

# Define functions:
program.add_func_decl(
    "legion_domain_point_get_point_1d", (legion_domain_point_t,), legion_point_1d_t
)
program.add_func_decl(
    "legion_domain_point_from_point_1d", (legion_point_1d_t,), legion_domain_point_t
)
program.add_func_decl(
    "legion_logical_partition_get_logical_subregion_by_color_domain_point",
    (legion_runtime_t, legion_logical_partition_t, legion_domain_point_t,),
    legion_logical_region_t,
)

# Define variables:
runtime = pt.Symbol(legion_runtime_t, "runtime")
parent = pt.Symbol(legion_logical_partition_t, "parent")
point = pt.Symbol(legion_domain_point_t, "point")
domain = pt.Symbol(legion_domain_t, "domain")
point1d = pt.Symbol(legion_point_1d_t, "point1d")
x = pt.Symbol(coord_t, "x")
x_plus_1 = pt.Symbol(coord_t, "x_plus_1")
point1d_x_plus_1 = pt.Symbol(legion_point_1d_t, "point1d_x_plus_1")
domain_point_x_plus_1 = pt.Symbol(legion_domain_point_t, "domain_point_x_plus_1")
result = pt.Symbol(legion_logical_region_t, "result")
point1d_x_plus_1_x = pt.Symbol(pt.ArrayType(coord_t, DIM), "point1d_x_plus_1_x")


program.add_func(
    "proj_functor",
    (runtime, parent, point, domain,),
    legion_logical_region_t,
    pt.Block(
        [
            pt.DefineVar(
                point1d, pt.Call("legion_domain_point_get_point_1d", [pt.Var(point)])
            ),
            pt.DefineVar(
                x, pt.GetElement(pt.GetElement(pt.Var(point1d), name="x"), idx=0)
            ),
            pt.DefineVar(x_plus_1, pt.Add(pt.Var(x), pt.Int64(1))),
            # Temporary array to change point1d_x_plus_1.x[0]
            pt.DefineVar(point1d_x_plus_1_x),
            pt.Assign(
                pt.Var(point1d_x_plus_1_x),
                pt.SetElement(pt.Var(point1d_x_plus_1_x), pt.Var(x_plus_1), 0),
            ),
            pt.DefineVar(point1d_x_plus_1),
            pt.Assign(
                pt.Var(point1d_x_plus_1),
                pt.SetElement(
                    pt.Var(point1d_x_plus_1), pt.Var(point1d_x_plus_1_x), name="x"
                ),
            ),
            pt.DefineVar(
                domain_point_x_plus_1,
                pt.Call(
                    "legion_domain_point_from_point_1d", [pt.Var(point1d_x_plus_1)]
                ),
            ),
            pt.DefineVar(
                result,
                pt.Call(
                    "legion_logical_partition_get_logical_subregion_by_color_domain_point",
                    [pt.Var(runtime), pt.Var(parent), pt.Var(domain_point_x_plus_1)],
                ),
            ),
            pt.Return(pt.Var(result)),
        ]
    ),
)


class ProjectionFunctor(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = program.compile()

        proj_functor = self.engine.get_function_address("proj_functor")
        self.proj_functor = cast(Callable[[], int], CFUNCTYPE(c_int32)(proj_functor))

        # self.proj_functor = cast(
        #     Callable[[int, int, int, int], int],
        #     CFUNCTYPE(c_int32, c_int32, c_int32, c_int32, c_int32)(proj_functor),
        # )


        # self.proj_functor = cast(
        #     Callable[
        #         [
        #             legion_runtime_t,
        #             legion_logical_partition_t,
        #             legion_domain_point_t,
        #             legion_domain_t,
        #         ],
        #         legion_logical_region_t,
        #     ],
        #     CFUNCTYPE(
        #         legion_runtime_t,
        #         legion_logical_partition_t,
        #         legion_domain_point_t,
        #         legion_domain_t,
        #         legion_logical_region_t,
        #     )(proj_functor)
        # )

    def test_proj_functor(self) -> None:
        self.assertEqual(self.proj_functor(), 0)
