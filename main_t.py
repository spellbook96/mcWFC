from Level import *
level = Level(USE_BATCHING=2000)

area = level.getBuildArea()
x_start = area[0]
z_start = area[1]
x_size = area[2]
z_size = area[3]
x_end = x_start + x_size
z_end = z_start + z_size
x_center = int((x_start + x_end) /2)
z_center = int((z_start + z_end) /2)

from building.pagoda import*
from Level import *
level = Level(USE_BATCHING=2000)

material_dict={}
material_dict["tree_ID"] = (17, 0)
material_dict["wood_ID"] = (5, 0)
material_dict["fence_id"] = (43, 3, 191)
material_dict["floor_id"] = (1, 6)
roof_ID = (109, 44, 5, 43, 5)
material_dict["roof_ID"] = roof_ID

area = level.getBuildArea()
x_start = area[0]
z_start = area[1]
x_size = area[2]
z_size = area[3]
x_end = x_start + x_size
z_end = z_start + z_size

p = Pagoda_builder(level, x_start,level.getHeightAt(x_start,z_start),z_start,
                            material_dict["tree_ID"][0],
                            material_dict["tree_ID"][1], material_dict["wood_ID"][0],
                            material_dict["wood_ID"][1],
                            material_dict["roof_ID"])

p.build()
level.flush()
import time

time.sleep(10)
print("undo")
level.undo()