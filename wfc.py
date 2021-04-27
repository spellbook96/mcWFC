import math
import random
import numpy as np
import copy
class WFC: #branch 0
    def __init__(self, x_size,y_size,z_size,buildingdata):
        #initialize
        begin_time = time()
        print("-------------------\ninitializing wfc")
        self.stationary = []
        self.blockList,PL,self.IDtoName,self.NametoID = buildingdata
        blockArr = np.array(self.blockList)
        y,z,x = blockArr.shape
        self.FMX = x_size
        self.FMY = y_size
        self.FMZ = z_size
        self.N = 3
        N=self.N
        # initialize pattern list and weights
        self.PList = list()
        PWeight = {}
        self.Pstep = 2


        from Prototypes import Prototype
        for _y in range(0,y-self.N,self.Pstep):
            for _z in range(0,z-self.N,self.Pstep):
                for _x in range(0,x-self.N,self.Pstep):
                    pattern = Prototype(self.N)
                    for ny in range(0,self.N):
                        for nz in range(0,self.N):
                            for nx in range(0,self.N):
                                pattern.blocks[ny][nz][nx]=blockArr[_y+ny][_z+nz][_x+nx]       
                                # print("pattern %s %s %s [%s]: %s"%(i,j,k,ni+nj*self.N+nk*self.N*self.N,pattern[ni+nj*self.N+nk*self.N*self.N]))

                    index = 0
                    for p in self.PList:
                        p = np.array(p.blocks)
                        if np.allclose(pattern.blocks,p):
                            break
                        index += 1
                    if (index == len(self.PList)):
                        # print("add： %s" %pattern)
                        self.PList.append(pattern)
                        PWeight[index] = 1

                    else:
                        PWeight[index] += 1

        # add dirt pattern
        # self.Dirt_i = len(self.PList)
        # dirtID = self.NametoID["minecraft:dirt"]
        # dirtP = Prototype(self.N)
        # for ny in range(0,self.N):
        #     for nz in range(0,self.N):
        #         for nx in range(0,self.N):
        #             dirtP.blocks[ny][nz][nx]=dirtID
        # self.PList.append(dirtP)
        # print(PWeight)
        self.T = len(self.PList)
        T = self.T
        self.propagator = [[[None]for _ in range(self.T)] for _ in range(6)]    #6*T*uncertain


        self.DX2 = [-self.Pstep,0,self.Pstep,0,0,0]
        self.DY2 = [0,self.Pstep,0,-self.Pstep,0,0]
        self.DZ2 = [0,0,0,0,self.Pstep,-self.Pstep]

        self.DX = [-1,0,1,0,0,0]
        self.DY = [0,1,0,-1,0,0]
        self.DZ = [0,0,0,0,1,-1]
        self.opposite = [2,3,0,1,5,4]

        def agrees(p1,p2,dx,dy,dz):
            xmin = 0 if dx < 0 else dx
            xmax = dx + N if dx < 0 else N
            ymin = 0 if dy < 0 else dy
            ymax = dy + N if dy < 0 else N
            zmin = 0 if dz < 0 else dz
            zmax = dz + N if dz < 0 else N

            for y in range(ymin,ymax):
                for z in range(zmin,zmax):
                    for x in range(xmin,xmax):
                        if p1[y][z][x] != p2[y-dy][z-dz][x-dx]:
                            return False
            return True

        self.Air_p = np.full((self.N,self.N,self.N),self.NametoID["minecraft:air"])
        self.Air_i = 0
        index =0
        for p in self.PList:
            if np.allclose(p.blocks,self.Air_p):
                self.Air_i = index
                break
            index+=1
        self.Dirt_p = np.full((self.N,self.N,self.N),self.NametoID["minecraft:dirt"])
        self.Dirt_i = 0
        index =0
        for p in self.PList:
            if np.allclose(p.blocks,self.Dirt_p):
                self.Dirt_i = index
                break
            index+=1
        for d in range(0,6):
            for t in range(0,T):
                l = list()
                for t2 in range(0,T):
                    if agrees(self.PList[t].blocks,self.PList[t2].blocks,self.DX2[d],self.DY2[d],self.DZ2[d]) :
                        l.append(t2)
                self.propagator[d][t] = [0 for _ in range(len(l))]
                for c in range(len(l)):
                    self.propagator[d][t][c] = l[c]
                if self.propagator[d][t]== []:
                    self.propagator[d][t]=[self.Air_i]
                #print("propagator for Pattern%s  direct%s is : %s" %(t,d,self.propagator[d][t]))


        self.wave = [[[[False for _ in range(T)]for _ in range(self.FMX)]for _ in range(self.FMZ)]for _ in range(self.FMY)]
        self.compatible = [[[[[0 for _ in range(6)]for _ in range(T)] for _ in range(self.FMX)]for _ in range(self.FMZ)]for _ in range(self.FMY)]
        self.observed = [[[None for _ in range(self.FMX)]for _ in range(self.FMZ)]for _ in range(self.FMY)]

        self.weights = [0 for _ in range(T) ]
        self.weightLogWeights = [0 for _ in range(T) ]
        self.sumOfWeights = 0
        self.sumOfWeightLogWeights = 0
    

        for t in range(T):
            self.weights[t] = PWeight[t]
            self.weightLogWeights[t] = self.weights[t] * math.log(self.weights[t])
            self.sumOfWeights += self.weights[t]
            self.sumOfWeightLogWeights += self.weightLogWeights[t]

        self.startingEntropy = math.log(self.sumOfWeights) - self.sumOfWeightLogWeights / self.sumOfWeights

        self.sumsOfOnes = [[[0 for _ in range(self.FMX)]for _ in range(self.FMZ)]for _ in range(self.FMY)]
        self.sumsOfWeights = [[[0 for _ in range(self.FMX)]for _ in range(self.FMZ)]for _ in range(self.FMY)]
        self.sumsOfWeightLogWeights = [[[0 for _ in range(self.FMX)]for _ in range(self.FMZ)]for _ in range(self.FMY)]
        self.entropies = [[[0 for _ in range(self.FMX)]for _ in range(self.FMZ)]for _ in range(self.FMY)]

        self.stack = [None for _ in range(self.FMX*self.FMY*self.FMZ*T)]
        self.stacksize = 0

        self.weights[self.Air_i] = 10
        self.weights[self.Dirt_i] = 1
        # Calculate run time
        end_time = time()
        run_time = end_time - begin_time
        print("runtime: %.2f s" % run_time)
        
    def OnBoundary(self,x, y, z):
        return ((x + self.N > self.FMX ) or (y + self.N > self.FMY) or (z + self.N > self.FMZ))

    def StuffRandom(self,source_array, random_value):
        a_sum = sum(source_array)
        
        for j in range(0, len(source_array)):
            source_array[j] /= a_sum
        i = 0
        x = 0
        while (i < len(source_array)):
            x += source_array[i]
            if random_value <= x:
                return i
            i += 1
        return 0

    def Ban(self,i,t):
        x,y,z = i
        #print("Ban (%s,%s)" %(i,t))
        self.wave[y][z][x][t] = False
        comp = self.compatible[y][z][x][t]
        for d in range(6):
            comp[d] = 0
        self.stack[self.stacksize] = (i,t)
        self.stacksize += 1

        self.sumsOfOnes[y][z][x] -= 1
        self.sumsOfWeights[y][z][x] -= self.weights[t]
        self.sumsOfWeightLogWeights[y][z][x] -= self.weightLogWeights[t]
        
        s = self.sumsOfWeights[y][z][x]
        self.entropies[y][z][x] = math.log(s) - self.sumsOfWeightLogWeights[y][z][x] / s

    def Propagate(self):
        while self.stacksize > 0:
            e1 = self.stack[self.stacksize-1]
            self.stacksize -= 1

            i1 = e1[0]
            x1,y1,z1=i1

            for d in range(6):
                dx,dy,dz = self.DX[d],self.DY[d],self.DZ[d]
                x2,y2,z2 = x1+dx,y1+dy,z1+dz
                if self.OnBoundary(x2,y2,z2):
                    continue
                if x2 < 0: 
                    x2 += self.FMX
                elif x2 >= self.FMX: 
                    x2 -= self.FMX
                if y2 < 0: 
                    y2 += self.FMY
                elif y2 >= self.FMY: 
                    y2 -= self.FMY
                if z2 < 0 :
                    z2 += self.FMZ
                elif y2 >= self.FMZ:
                    z2 -= self.FMZ

                i2 = (x2,y2,z2)
                p = self.propagator[d][e1[1]]
                compat = self.compatible[y2][z2][x2]

                for l in range(len(p)):
                    t2 = p[l]
                    comp = compat[t2]

                    comp[d] -= 1
                    if comp[d] ==0:

                        # if self.Vflag:
                        #     print("pattern %s at (%d,%d,%d)" % (t2,self.Vx+x2,self.Vy+y2,self.Vz+z2))
                        #     pt = self.PList[t2].blocks
                        #     for _y in range(self.N):
                        #         for _z in range(self.N):
                        #             for _x in range(self.N):
                        #                 self.level.setBlock(_x+self.Vx+x2,_y+self.Vy+y2,_z+z2+self.Vz,self.IDtoName[pt[_y][_z][_x]])
                        #     self.level.flush()
                        self.Ban(i2,t2)

    def Observe(self):
        obsmin = 1E+3
        argmin = -1

        for y in range(self.FMY):
            for z in range(self.FMZ):
                for x in range(self.FMX):
                    
                    if self.OnBoundary(x,y,z):
                        continue
                    amount = self.sumsOfOnes[y][z][x]
                    if amount == 0:
                        return False
                    entropy = self.entropies[y][z][x]
                    if amount >1 and entropy <= obsmin:
                        noise = 1e-6 * random.random()
                        if entropy + noise < obsmin:
                            obsmin = entropy + noise
                            argmin = (x,y,z)
        
        if argmin == -1:
            self.observed = [[[None for _ in range(self.FMX)]for _ in range(self.FMZ)]for _ in range(self.FMY)]
            for y in range(self.FMY):
               for z in range(self.FMZ):
                for x in range(self.FMX):
                    for t in range(self.T):
                        if (self.wave[y][z][x][t]):
                            self.observed[y][z][x] = t 
                            break
            return True
        
        distribution = [0 for _ in range(0,self.T)]
        x,y,z = argmin
        for t in range(0,self.T):
            distribution[t] = self.weights[t] if self.wave[y][z][x][t] else 0
        r = self.StuffRandom(distribution, random.random())

        w = self.wave[y][z][x]

        for t in range(0,self.T):
            if w[t] != (t == r):
                self.Ban(argmin,t)
        
        # if self.Vflag:
        #     print("pattern %s at (%d,%d,%d)" % (r,self.Vx+x,self.Vy+y,self.Vz+z))
        #     p = self.PList[r].blocks
        #     for _y in range(self.N):
        #         for _z in range(self.N):
        #             for _x in range(self.N):
        #                 self.level.setBlock(_x+self.Vx+x,_y+self.Vy+y,_z+z+self.Vz,self.IDtoName[p[_y][_z][_x]])
        #     self.level.flush()
        return None    

    def Clear(self):
        for y in range(self.FMY):
               for z in range(self.FMZ):
                    for x in range(self.FMX):
                        for t in range(self.T):
                            self.wave[y][z][x][t] = True
                            for d in range(6):
                                self.compatible[y][z][x][t][d] = len(self.propagator[self.opposite[d]][t])
                    
                        self.sumsOfOnes[y][z][x] = len(self.weights)
                        self.sumsOfWeights[y][z][x] = self.sumOfWeights
                        self.sumsOfWeightLogWeights[y][z][x] = self.sumOfWeightLogWeights
                        self.entropies[y][z][x] = self.startingEntropy

        for x in range(self.FMX):
            for z in range(self.FMZ):
                for t in range(self.T):
                    if t!=self.Dirt_i:
                        self.Ban((x,0,z),t)
                for y in range(1,self.FMY):
                    self.Ban((x,y,z),self.Dirt_i)
        self.Propagate()

    def run(self,level = None,visualize=False):
        begin_time = time()
        print("-------------------\nrunning wfc")
        # visualize init
        self.Vflag = False
        if visualize == True:
            self.Vflag = True
            Vn = 0
            self.level = level
            area = self.level.getBuildArea()
            x_start = area[0]
            z_start = area[1]
            x_size = area[2]
            z_size = area[3]
            x_end = x_start + x_size
            z_end = z_start + z_size
            self.Vx = int((x_start + x_end) /2)
            self.Vz = int((z_start + z_end) /2)
            # self.Vy = int(self.level.getHeightAt(self.Vx,self.Vz))
            self.Vy = 4
            print("building at %d %d %d" %(self.Vx,self.Vy,self.Vz))
            for y in range(self.FMY*self.Pstep):
                for z in range(self.FMZ*self.Pstep):
                  for x in range(self.FMX*self.Pstep):
                      self.level.setBlock(self.Vx+x,self.Vy+y,self.Vz+z,"glass")
            self.level.flush()

        #init process bar
        process_c =0
        process_cM = 1
        process_n = self.FMX*self.FMZ*self.FMY*(self.T-1)
        self.Clear()
        self.process_bar(0,start_str='',end_str='100%', total_length=15)
        while 1:
            result = self.Observe()
            if (result != None):
                self.process_bar(1,start_str='',end_str='100%', total_length=15)
                if self.Vflag == True:
                    self.preview()
                # Calculate run time
                end_time = time()
                run_time = end_time - begin_time
                print("\nruntime: %.2f s" % run_time)
                return result
            self.Propagate()
            process_c+=1
            if process_c ==process_cM:
                process_c =0
                percent = (self.FMX*self.FMZ*self.FMY*self.T-np.sum(self.wave))/process_n
                self.process_bar(percent,start_str='',end_str='100%', total_length=15)
        return True

    def preview(self):
        #import pdb; pdb.set_trace()
        for _y in range(self.FMY):
            for _z in range(self.FMZ):
                for _x in range(self.FMX):
                    if np.sum(self.wave[_y][_z][_x])==1:
                        for t in range(len(self.PList)):
                            if self.wave[_y][_z][_x][t]==True:
                                p = self.PList[t].blocks
                                for y in range(self.Pstep):
                                    for z in range(self.Pstep):
                                        for x in range(self.Pstep):
                                            self.level.setBlock(_x*self.Pstep+self.Vx+x,_y*self.Pstep+self.Vy+y,_z*self.Pstep+z+self.Vz,self.IDtoName[p[y][z][x]])
                                

    def process_bar(self,percent, start_str='', end_str='', total_length=0):
        bar = ''.join(["\033[31m%s\033[0m"%'▋▋'] * int(percent * total_length)) + ''
        bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent*100) + end_str
        print(bar, end='', flush=True)

    def getPList(self,n=10):
        result=[]
        PData = [[[0 for _ in range(self.N)] for _ in range(self.N)] for _ in range(self.N)]
        for i in range(n):
            for y in range(self.N):
                for z in range(self.N):
                    for x in range(self.N):
                        PData[y][z][x]=self.IDtoName[self.PList[i].blocks[y][z][x]]
            result.append(copy.deepcopy(PData))

        return result

    def getPrototypes(self,level):
        from Prototypes import Prototypes
        prototypes =Prototypes(self.getPList(len(self.PList)),self.N,level)
        return prototypes

    def getIDtoName(self):
        return self.IDtoName

if __name__ == "__main__":
    from buildingData import *
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

    bd = buildingData(level,filename="t_r1.txt")
    bdData = bd.getBuildingData()
    wfc = WFC(20,20,20,bdData)
    r = wfc.run(level=level,visualize=True)
    print(r)
    # prototypes = wfc.getPrototypes(level)
    # prototypes.show(x_center,4,z_center)
    # # n =0
    
    
    level.flush()
    # import time

    # time.sleep(10)
    # print("undo")
    # level.undo()