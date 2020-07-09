#define LEGION_ENABLE_C_BINDINGS
#include "legion.h"

// for x in D:
//     my_task(p[x + 1])
legion_logical_region_t my_projection_functor(
      legion_runtime_t runtime,
      legion_logical_partition_t parent, // p
      legion_domain_point_t point, // x
      legion_domain_t domain) // D
{
  // legion_point_1d_t is a struct
  // legion_point_1d_t.x is an array
  legion_point_1d_t point1d = legion_domain_point_get_point_1d(point);
  coord_t x = point1d.x[0];
  coord_t x_plus_1 = x + 1;
  legion_point_1d_t point1d_x_plus_1;
  point1d_x_plus_1.x[0] = x_plus_1;
  legion_domain_point_t domain_point_x_plus_1 = legion_domain_point_from_point_1d(point1d_x_plus_1);
  legion_logical_region_t result = legion_logical_partition_get_logical_subregion_by_color_domain_point(runtime, parent, domain_point_x_plus_1);
  return result;
}
