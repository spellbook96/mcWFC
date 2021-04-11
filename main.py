import random

import mapUtils
import interfaceUtils
from worldLoader import WorldSlice
from nbt import *

area = (0, 0, 128, 128)  # default build area
USE_BATCHING = True
buildArea = interfaceUtils.requestBuildArea()
if buildArea != -1:
    x1 = buildArea["xFrom"]
    z1 = buildArea["zFrom"]
    x2 = buildArea["xTo"]
    z2 = buildArea["zTo"]
    # print(buildArea)
    area = (x1, z1, x2-x1, z2-z1)

print("Build area is at position %s, %s with size %s, %s" % area)

worldSlice = WorldSlice(area)

heightmap = mapUtils.calcGoodHeightmap(worldSlice)


def heightAt(x, z):
    return heightmap[(x - area[0], z - area[1])]


def setBlock(x, y, z, block):
    if USE_BATCHING:
        interfaceUtils.placeBlockBatched(x, y, z, block, 100)
    else:
        interfaceUtils.setBlock(x, y, z, block)

x_start =area[0]
z_start =area[1]
x_size =area[2]
z_size =area[3]

from buildingData import *
writeData(worldSlice,[130,4,13],[154,45,37],"tower")
# b = buildingData("tower.txt")
# #b.build(0,4,0)
# b.clear(0,4,0)