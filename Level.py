import random
from typing import Any, Union

import mapUtils
import interfaceUtils
from worldLoader import WorldSlice
from nbt import *

# import ICE.HeightMap as H
# import ICE.FlatFinder as F
# import ICE.BorderAreaFinder as S
# import ICE.GravityFinder as G
# import ICE.Pioneer as P
# from ICE.Shrine import *
# from ICE.pagoda import *
# from time import *
# from ICE.MountainPath import *
# from ICE.Laying import *
import numpy as np
from matplotlib import pyplot as plt
from Quadtree import *
import json


class Level:
    def __init__(self, USE_BATCHING=2000,hm=True):
        print("initializing")
        begin_time = time()
        self.area = (0, 0, 128, 128)  # default build area
        self.USE_BATCHING = USE_BATCHING
        self.hm=hm
        buildArea= interfaceUtils.requestBuildArea()
        if buildArea != -1:
                x1 = buildArea["xFrom"]
                z1 = buildArea["zFrom"]
                x2 = buildArea["xTo"]
                z2 = buildArea["zTo"]
                # print(buildArea)
                self.area = (x1, z1, x2 - x1, z2 - z1)
        print("Build area is at position %s, %s with size %s, %s" % self.area)
        self.worldSlice = WorldSlice(self.area)
        if hm:
            self.calculate_Quadtree()
            
        self.undo_flag = True
        self.undo_blocks = []
        self.tmp = []
        self.id_dict = {}
        f = open("id_dict.json", "r", encoding="utf-8")
        self.id_dict = json.loads(f.read())
        f.close()
        # Calculate run time
        end_time = time()
        run_time = end_time - begin_time
        print("runtime: %.2f s" % run_time)

    def calculate_Quadtree(self,mgw =1,mfw=1,qms = 10,qi=2):
        if not self.hm:
            buildArea= interfaceUtils.requestBuildArea()
            if buildArea != -1:
                x1 = buildArea["xFrom"]
                z1 = buildArea["zFrom"]
                x2 = buildArea["xTo"]
                z2 = buildArea["zTo"]
                # print(buildArea)
                self.area = (x1, z1, x2 - x1, z2 - z1)
            
            self.worldSlice = WorldSlice(self.area)
        self.heightmap = mapUtils.calcGoodHeightmap(self.worldSlice)
        self.calculate_gradient()
        self.Q = Quadtree(self,mgw,mfw,qms,qi)

    def getBuildArea(self):
        return self.area

    def getHeightMap(self):
        return self.heightmap

    def getQuadtree(self):
        return self.Q.Quadtree_result
        
    def getQuadtreeList(self):
        return self.Q.QuadtreeList
        
    def calculate_gradient(self):
        res = np.gradient(self.heightmap)
        self.height_map_gradient_X = res[0]
        self.height_map_gradient_Z = res[1]
        self.gradientMap = np.sqrt(res[0] ** 2 + res[1] ** 2)

    def getGradientMap(self):
        return self.gradientMap

    def getBlockAt(self, x, y, z):
        block = self.worldSlice.getBlockAt((int(x), int(y), int(z)))
        return block

    def getBlockCompoundAt(self, x, y, z):
        return self.worldSlice.getBlockCompoundAt((x, y, z))

    def plotMap(self):
        self.Q.plotMap()

    def getHeightAt(self, x, z):
        return self.heightmap[(x - self.area[0], z - self.area[1])]

    def setBlock(self, x, y, z, block):
        if self.undo_flag:
            tmp = self.getBlockAt(x, y, z)
            self.undo_blocks.append([[x, y, z], tmp])

        x = int(x)
        y = int(y)
        z = int(z)
        if self.USE_BATCHING:
            interfaceUtils.placeBlockBatched(x, y, z, block, self.USE_BATCHING)
        else:
            interfaceUtils.setBlock(x, y, z, block)

    def setBlockID(self, x, y, z, blockid, data=0):
        
        bid = str(blockid) + "," + str(data)
        if bid in self.id_dict:
            try:
                self.setBlock(x, y, z, self.id_dict[bid])
            except:
                print("SET_BOLCK_ID ERROR:%d %d %d id=%s" % (x, y, z, self.id_dict[bid]))
        else:
            self.tmp.append([x, y, z, blockid, data])
            # print("NOT EXIST:%d %d %d id=%d,%d" % (x, y, z, blockid,data))
            print("NOT EXIST:id=%d,%d" % (blockid,data))

    def print_blockID(self):
        with open("BlockID.txt", 'w') as f:
            for line in self.tmp:
                [x, y, z, blockid, data] = line
                # f.write("%d %d %d id=%s,data=%s\n"% (x,y,z,blockid,data))
                f.write("id=%s,data=%s\n" % (blockid, data))

    def flush(self, batch=100):
        self.undo_flag = False
        # batch = self.USE_BATCHING
        # for i in range(batch):
        #     self.setBlock(0, 100, 0, "air")
        interfaceUtils.sendBlocks()
        self.undo_flag = True

    def undo(self):
        self.undo_flag = False
        for block in self.undo_blocks:
            x, y, z = block[0]
            self.setBlock(x, y, z, block[1])
        self.flush()
        self.undo_flag = True


if __name__ == "__main__":

    level = Level(USE_BATCHING=2000)

    area = level.getBuildArea()
    x_start = area[0]
    z_start = area[1]
    x_size = area[2]
    z_size = area[3]
    x_end = x_start + x_size
    z_end = z_start + z_size

    from buildingData import writeData, buildingData
    # writeData(level,[130,4,13],[154,50,37],filename="tower.txt")
    # b = buildingData(level,filename="tower.txt")
    # b.build(x_start,level.getHeightAt(x_start,z_start),z_start)

    # from building.field_builder import field
    # f = field(level,262,69,70,50,50,1,2)
    # f.build()
    from Cityscape import *

    c = Cityscape(level, 50, 216, 4, 80, 1, 24, 0, 5, 2, (180, 182, 0, 179, 0))
    c.build()
    level.print_blockID()
    
    import time

    time.sleep(20)
    print("undo")
    level.undo()

    # level.plotMap()

    print("finished")
