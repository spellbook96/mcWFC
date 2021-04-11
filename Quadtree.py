import numpy as np
from matplotlib import pyplot as plt
from time import *


class Quadtree:
    def __init__(self, level):
        # begin_time = time()

        # Set weight
        self.regard_as_obstruction_weigth = 0.7
        self.median_gradientMap_weigth = 4
        self.median_freq_y_map_weigth = 7
        self.median_final_weigth = 3
        self.Quadtree_min_of_size = 5
        self.Quadtree_ignore = 5

        # init
        area = level.getBuildArea()
        self.level = level
        self.x_s = area[0]
        self.z_s = area[1]
        self.x_size = area[2]
        self.z_size = area[3]
        self.x_e = self.x_s + self.x_size
        self.z_e = self.z_s + self.z_size
        self.block_name = np.zeros(200)
        self.frequency = np.zeros(128, dtype=np.int)
        self.water_lava_blocks = np.ones(
            (self.x_size, self.z_size), dtype=np.int)
        self.heightmap = self.level.getHeightMap()
        self.gradientMap = self.level.getGradientMap()
        self.check()

        # Find obstruction
        self.gradientMap_F = self.median_filter(
            self.gradientMap, self.median_gradientMap_weigth)
        self.wall = np.where(self.regard_as_obstruction_weigth >
                             self.gradientMap_F, 1, self.gradientMap_F)
        self.wall = np.where(1 != self.wall, 0, self.wall)
        self.obstruction = self.water_lava_blocks*self.wall

        self.wall2=np.where(self.regard_as_obstruction_weigth>self.gradientMap,1,self.gradientMap)
        self.wall2=np.where(1!=self.wall2,0,self.wall2)
        self.obstruction2=self.water_lava_blocks*self.wall2

        # Find most frequent y
        self.freq_y=self.most_freq_y()
        self.freq_y_map=self.most_freq_y_map()

        # Find no obstruction map at the most frequent y map
        self.freq_y_map=self.median_filter(self.freq_y_map,self.median_freq_y_map_weigth)
        self.final=self.median_filter(self.obstruction,self.median_final_weigth)
        self.find_map=self.freq_y_map*self.final

        # Find usable maps with Quadtree
        self.Quadtree=[]
        self.Quadtree_Finder((self.final-1)*(-1),0,len(self.final)-1,0,len(self.final[0])-1)
        self.Quadtree_result = np.zeros((self.x_size, self.z_size), dtype=np.int)
        for i in self.Quadtree:
            self.Quadtree_result[i[0],i[1]]=1

        # # Calculate run time
        # end_time = time()
        # run_time = end_time - begin_time
        # print ("Quadtree runtime: %.2f s" % run_time)
    def check(self):
        for x in range(self.x_size):
            for z in range(self.z_size):
                block = self.level.getBlockAt(
                    x+self.x_s, self.heightmap[x, z]-1, z+self.z_s)
                if block[-5:] == 'water' or block[-4:] == "lava":
                    self.water_lava_blocks[x, z] = 0

    def plotMap(self):
        # Plot map
        plt.subplot(2,2,2)
        plt.imshow(self.wall, cmap='gray')
        plt.subplot(2,2,1)
        plt.imshow(self.heightmap, cmap='gray')
        plt.subplot(223)
        plt.imshow(self.water_lava_blocks, cmap='gray')
        # plt.subplot(245)
        # plt.imshow(self.obstruction, cmap='gray')
        # plt.subplot(246)
        # plt.imshow(self.freq_y_map, cmap='gray')
        plt.subplot(224)
        plt.imshow(self.Quadtree_result, cmap='gray')
        # plt.subplot(248)
        # plt.imshow(self.final, cmap='gray')
        plt.show()

        

    def median_filter(self, data, kernel_size):
        temp = []
        indexer = kernel_size // 2
        # print(len(data),len(data[0]))
        data_final = np.zeros((len(data), len(data[0])))
        for i in range(len(data)):
            for j in range(len(data[0])):
                for z in range(kernel_size):
                    if i+z-indexer < 0 or i+z-indexer > len(data)-1:
                        for c in range(kernel_size):
                            temp.append(0)
                    else:
                        if j+z-indexer < 0 or j+indexer > len(data[0])-1:
                            temp.append(0)
                        else:
                            for k in range(kernel_size):
                                temp.append(data[i+z-indexer][j+k-indexer])
                temp.sort()
                data_final[i][j] = temp[len(temp)//2]
                temp = []
        return data_final

    def most_freq_y(self):
        sum=[]
        freq_y=0
        max_freq=0
        for x in range(0, self.x_size):
            for z in range(0, self.z_size):
                if self.obstruction[x,z]==1:
                    self.frequency[self.heightmap[x,z]]+=1
        for i in range(2,126):
            sum.append(self.frequency[i-2]+self.frequency[i-1]+self.frequency[i]+self.frequency[i+1]+self.frequency[i+2])
        
        max_freq=sum.count(max(sum))

        if max_freq>1:
            count=int(max_freq/2)
            for i in range(0,124):
                if sum[i]==max(sum):count-=1
                if count==0: break
            freq_y=i+2
        elif max_freq==1:freq_y=sum.index(max(sum))+2

        return freq_y

    def most_freq_y_map(self):
        freq_y_map = np.zeros((self.x_size, self.z_size), dtype=np.int)
        jud=[self.freq_y-2,self.freq_y-1,self.freq_y,self.freq_y+1,self.freq_y+2]
        for x in range(0, self.x_size):
            for z in range(0, self.z_size):
                if self.heightmap[x,z] in jud:
                    freq_y_map[x,z]=1
        return freq_y_map 



    def Quadtree_Finder(self,data,x_s,x_e,y_s,y_e):
        x=x_e-x_s+1
        y=y_e-y_s+1
        a=x//2
        b=y//2
        if (x**2+y**2)**0.5<=self.Quadtree_min_of_size: 
            return 0

        if np.sum(data[x_s:x_e+1,y_s:y_e+1])<=self.Quadtree_ignore:
            for i in range(x_s,x_e+1):
                for j in range(y_s,y_e+1):
                    self.Quadtree.append([i,j])
            return 0

        self.Quadtree_Finder(data,x_s,x_s+a-1,y_s,y_s+b-1)
        self.Quadtree_Finder(data,x_s+a,x_e,y_s,y_s+b-1)
        self.Quadtree_Finder(data,x_s,x_s+a-1,y_s+b,y_e)
        self.Quadtree_Finder(data,x_s+a,x_e,y_s+b,y_e)