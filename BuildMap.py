#!/usr/bin/python
# -*- coding: UTF-8 -*-
from matplotlib import pyplot as plt
import numpy as np
from numpy.core.defchararray import center
from numpy.core.shape_base import block
from numpy.testing._private.utils import build_err_msg
import random
from time import *

class BuildMap():

    def __init__(self,hm):
        begin_time = time() 
        self.result = self.calculate(hm)
        self.RoadList = self.makeRoadList(self.result)
        end_time = time()
        run_time = end_time - begin_time
        print ("BuildMap runtime: %.2f s" % run_time)


    def getRoadList(self):
        return self.RoadList

    def getMap(self):
        return self.result

    def makeRoadList(self,make_point):
        center_road = self.center_road_return(make_point)
        road_return_list = self.road_return_list(center_road)
        return road_return_list

    def calculate(self,hm):
        original = hm
        start_point = self.find_start_point(original)
        build_road = self.build_road(original,start_point)
        check_block = self.check_block(build_road)
        make_point = self.make_point(check_block)
        

        return make_point

        
    def make_block(self,result):
        for i in range(len(result)):
            for j in range(len(result[i])):
                if i%32 == 0:
                    result[i][j] = result[i][j]+1
                elif j%32 == 0:
                    result[i][j] = result[i][j]+1
        return result

    def check_block(self,result):
        k = 900#这个值可以调整建筑对地形要求的 敏感度 值越大对地形要求越高 可以建的房子越少（不可以超过1000）

        a = int(len(result)/32)
        b = int(len(result[0])/32)
        check_point = np.zeros((a,b))
        for i in range(a):
            for j in range(b):
                for ii in range(32):
                    for jj in range(32):
                        check_point[i][j]=check_point[i][j]+ result[i*32+ii][j*32+jj]
                if check_point[i][j] > k:
                    check_point[i][j] = 5
                else:
                    check_point[i][j] = 0


        for k in range(a):
            for j in range(b):
                for kk in range(32):
                    for jj in range(32):
                        result[k*32+kk][j*32+jj] = result[k*32+kk][j*32+jj] + check_point[k][j]

        return result

    def make_point(self,result):
        a = int(len(result)/32)
        b = int(len(result[0])/32)

        for f in range(a):
            for g in range(b):
                if result[f*32+1][g*32+1] > 4:
                    if result[(f-1)*32+1][g*32]==10 or result[f*32+1][(g-1)*32+1]==10:
                        result[f*32+1][g*32+1] = 20
                    else:
                        result[f*32+1][g*32+1] = 10
        return result

    def check_filter(self,result):
        a = int(len(result)/32)
        b = int(len(result[0])/32)
        check_point = np.zeros((a,b))
        for i in range(a):
            for j in range(b):
                for ii in range(32):
                    for jj in range(32):
                        check_point[i][j]=check_point[i][j]+ result[i*32+ii][j*32+jj]
        check_filter = np.zeros((a-2,b-2))
        for k in range(a-2):
            for g in range(b-2):
                check_filter[k][g]=(check_point[k][g]+check_point[k+1][g]+check_point[k][g+1]+check_point[k+1][g+1]+check_point[k+1][g+2]+check_point[k+2][g+1]+check_point[k+2][g+2]+check_point[k+2][g]+check_point[k][g+2])/9
                
        return check_filter

    def find_start_point(self,result):
        a = 1
        b = 1
        
        check_filter= result
        for i in range(len(check_filter)):
            for j in range(len(check_filter[i])):
                if i>0 and j >0:
                    if check_filter[i][j]+check_filter[i][j-1]+check_filter[i-1][j]+check_filter[i-1][j-1]>check_filter[a][b]+check_filter[a][b-1]+check_filter[a-1][b]+check_filter[a-1][b-1]:
                        a = i
                        b = j
        a = a*32
        b = b*32
        start_point =[a,b]
        return start_point

    def plotMap(self):

        plt.imshow(self.result)
        plt.show()

        

    def build_road_tree(self,make_block,start_point):
        a = start_point[0]
        b = start_point[1]
        k = 7 #这个值可以调整路的稠密稀疏程度（不可以小于5）
        next_point = [a,b]
        for i in range(k):
            if i<5: 
                flag = random.randint(0,3)
                if flag == 0:
                    a = a+32
                elif flag == 1:
                    a = a-32
                elif flag == 2:
                    b = b-32
                elif flag == 3:
                    b = b+32
            else :
                flag = random.randint(0,3)
                if flag == 0:
                    a = a+16
                elif flag == 1:
                    a = a-16
                elif flag == 2:
                    b = b-16
                elif flag == 3:
                    b = b+16
            next_point = next_point+[a,b]
            # next_point = check_road(next_point,make_block)

            l = len(next_point)
            point_1 = next_point[l-4]
            point_2 = next_point[l-3]
            point_3 = next_point[l-2]
            point_4 = next_point[l-1]
            while point_1 != point_3 or point_2!= point_4:
                if point_1<point_3:
                    point_1 = point_1 + 1
                elif point_1>point_3:
                    point_1 = point_1 - 1
                elif point_2<point_4:
                    point_2 = point_2 + 1
                elif point_2>point_4:
                    point_2 = point_2 - 1
                try:
                    make_block[point_1][point_2] = -10
                except:
                    pass
        return make_block
                
    def build_road(self,make_block,start_point):
        k = 5 #这个值可以调整路的总量
        for i in range(k):
            make_block = self.build_road_tree(make_block,start_point)

        return make_block

    def road_mark_11(self,make_block):
        for i in range(1,len(make_block)-1):
            for j in range(1,len(make_block[i])-1):
                if make_block[i][j] == -10:
                    if make_block[i-1][j] == -10 and make_block[i+1][j] == -10 :
                        make_block[i][j] = -11
        return make_block

    def road_mark_12(self,make_block):
        for i in range(1,len(make_block)-1):
            for j in range(1,len(make_block[i])-1):
                if make_block[i][j] == -10:
                    if make_block[i][j+1] == -10 and make_block[i][j-1] == -10 :
                        make_block[i][j] = -12
        return make_block

    def road_mark_13(self,make_block):
        for i in range(1,len(make_block)-1):
            for j in range(1,len(make_block[i])-1):
                if make_block[i][j] == -10:
                    if make_block[i+1][j] < -10 and make_block[i][j+1] < -10 :
                        make_block[i][j] = -13
        return make_block

    def road_mark_14(self,make_block):
        for i in range(1,len(make_block)-1):
            for j in range(1,len(make_block[i])-1):
                if make_block[i][j] == -10:
                    if make_block[i-1][j] < -10 and make_block[i][j-1] < -10 :
                        make_block[i][j] = -14
        return make_block

    def road_mark_15(self,make_block):
        for i in range(1,len(make_block)-1):
            for j in range(1,len(make_block[i])-1):
                if make_block[i][j] == -10:
                    if make_block[i+1][j] < -10 and make_block[i][j-1] < -10 :
                        make_block[i][j] = -15
        return make_block

    def road_mark_16(self,make_block):
        for i in range(1,len(make_block)-1):
            for j in range(1,len(make_block[i])-1):
                if make_block[i][j] == -10:
                    if make_block[i-1][j] < -10 and make_block[i][j+1] < -10 :
                        make_block[i][j] = -16
        return make_block
    
    # 
    def center_road_return(self,make_point):
        for i in range(1,len(make_point)-1):
            for j in range(1,len(make_point[i])-1):
                
                if make_point[i][j] >= 5 and make_point[i][j+1] < 5 and make_point[i][j] != 30:
                    make_point[i][j+1]=30
                    make_point[i][j+2]=30
                    make_point[i][j+3]=30
                elif make_point[i][j] >= 5 and make_point[i-1][j] < 5:
                    make_point[i-1][j]=30
                    make_point[i-2][j]=30
                    make_point[i-3][j]=30
        return make_point

    def road_return_list(self,make_point):
        return_list = []
        for i in range(1,len(make_point)-1):
            for j in range(1,len(make_point[i])-1):
                if make_point[i][j] == 10 or make_point[i][j] == 20:
                    if make_point[i][j+32] !=10 or make_point[i][j+32] !=20:
                        start_y = j
                        start_x = i-1
                        end_y = j+32
                        end_x = i-1
                        size_y = 32
                        size_x = 3
                        n=0
                        e=1
                        s=0
                        w=0
                        # make_point[start_x][start_y] = 200
                        # make_point[end_x][end_y] = 500
                        return_list.append([start_x,start_y,end_x,end_y,size_x,size_y,n,e,s,w])
                    if make_point[i+32][j] !=10 or make_point[i+32][j+32] !=20:
                        start_y = j+33
                        start_x = i
                        end_y = j+33
                        end_x = i+32
                        size_y = 3
                        size_x = 32
                        # make_point[start_x][start_y] = 200
                        # make_point[end_x][end_y] = 200
                        n=0
                        e=0
                        s=1
                        w=0
                        return_list.append([start_x,start_y,end_x,end_y,size_x,size_y,n,e,s,w])
                
        return return_list
                        
#上面有三个可以自由调整的K值
# 1:首先给标注1坐标的位置上加地砖，做的函数能直观表现出来
# （lee的quad函数值稍微调大一些能否有更好的效果？）
# <0:道路（郊区规划比较多的路，如果给路两边适当增加小房子可能不错？）
# 20:公园（或小房子）
# 10:大型建筑
##

if __name__ == "__main__":
    from Level import *
    level = Level(USE_BATCHING=1000)

    area = level.getBuildArea()
    x_start = area[0]
    z_start = area[1]
    x_size = area[2]
    z_size = area[3]
    x_end = x_start + x_size
    z_end = z_start + z_size
    x_center = int((x_start + x_end) /2)
    z_center = int((z_start + z_end) /2)
    # level.plotMap()
    m = BuildMap(level.getQuadtree())
    # m.plotMap()
    bm = m.result
    qm = level.getQuadtree()
    for z in range(z_size):
        for x in range(x_size):
            # if bm[x,z]==1:
            #     level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"stone_brick_slab")
            if qm[x,z]==1:
                level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"stone_brick_slab")
            if bm[x,z]<0:
                level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"minecraft:gold_block")

    level.flush()
    import time

    time.sleep(20)
    print("undo")
    level.undo()