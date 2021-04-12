import math
import random
import numpy as np
import copy
class WFC:
    def __init__(self, x_size,y_size,z_size,buildingdata):
        #initialize

        self.stationary = []
        
        self.blockList,PL,self.IDtoName,self.NametoID = buildingdata
        blockArr = np.array(self.blockList)
        y,z,x = blockArr.shape
        self.FMX = x_size
        self.FMY = y_size
        self.FMZ = z_size
        self.T = 2
        self.N = 3

        # initialize pattern list and weights
        self.PList = list()
        PWeight = {}

        for _y in range(0,y-self.N):
            for _z in range(0,z-self.N):
                for _x in range(0,x-self.N):
                    pattern = np.zeros([self.N,self.N,self.N],dtype=int)
                    for ny in range(0,self.N):
                        for nz in range(0,self.N):
                            for nx in range(0,self.N):
                                pattern[ny][nz][nx]=blockArr[_y+ny][_z+nz][_x+nx]       
                                # print("pattern %s %s %s [%s]: %s"%(i,j,k,ni+nj*self.N+nk*self.N*self.N,pattern[ni+nj*self.N+nk*self.N*self.N]))

                    index = 0
                    for p in self.PList:
                        p = np.array(p)
                        if np.allclose(pattern,p):
                            break
                        index += 1
                    if (index == len(self.PList)):
                        # print("add： %s" %pattern)
                        self.PList.append(pattern)
                        PWeight[index] = 1

                    else:
                        PWeight[index] += 1
        # tmp =np.array(self.PList[0])
        # print(self.PList[0])
        # print(PWeight)

    def getPList(self,n=10):
        result=[]
        PData = [[[0 for _ in range(self.N)] for _ in range(self.N)] for _ in range(self.N)]
        for i in range(n):
            for y in range(self.N):
                for z in range(self.N):
                    for x in range(self.N):
                        PData[y][z][x]=self.IDtoName[self.PList[i][y][z][x]]
            result.append(copy.deepcopy(PData))

        return result

    def getPrototype(self,level):
        from Prototype import Prototype
        prototype =Prototype(self.getPList(len(self.PList)),self.N,level)
        return prototype

    def getIDtoName(self):
        return self.IDtoName

if __name__ == "__main__":
    from buildingData import *
    from Level import *
    level = Level(USE_BATCHING=100)
    area = level.getBuildArea()
    x_start = area[0]
    z_start = area[1]
    x_size = area[2]
    z_size = area[3]
    x_end = x_start + x_size
    z_end = z_start + z_size

    bd = buildingData(level,filename="house.txt")
    bdData = bd.getBuildingData()
    wfc = WFC(15,15,15,bdData)

    prototype = wfc.getPrototype(level)
    prototype.show(298,4,137)
    # prototypes = wfc.getPList()
    # n =0
    
    
    # level.flush()
    # import time

    # time.sleep(10)
    # print("redo")
    # level.redo()