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

from buildingData import writeData, buildingData

b = buildingData(level,filename="house.txt")
b.build(x_center,level.getHeightAt(x_center,z_center),z_center)


import time

time.sleep(10)
print("redo")
level.redo()