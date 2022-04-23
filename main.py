from Level import *
import random
from Cityscape import *
from buildingData import *
def include_list(a,b):
    tmp=[]
    tmp1 =[]
    for p in a:
        x = p[0][0]
        z = p[0][1]
        size=(p[1][0],p[1][1])
        for _p in b:
            _x = _p[0][0]
            _z = _p[0][1]
            _size=(_p[1][0],_p[1][1])
            if (x>_x and x<(_x+_size[0])) and z>_z and(z<(_z+_size[1])):
                tmp.append(p)
                break
    for p in a:
        if p not in tmp:
            tmp1.append(p)

    return tmp,tmp1

def is_sand(level,x,y,z):
    print(level.getBlockAt(x,y,z))
    return "minecraft:sand" == level.getBlockAt(x,y,z)

level = Level(USE_BATCHING=2000,hm=False)
level.calculate_Quadtree(mgw =10,mfw=2,qms = 40,qi=5)

area = level.getBuildArea()
x_start = area[0]
z_start = area[1]
x_size = area[2]
z_size = area[3]
x_end = x_start + x_size
z_end = z_start + z_size
x_center = int((x_start + x_end) /2)
z_center = int((z_start + z_end) /2)

qm = level.getQuadtree()
#level.plotMap()
for z in range(z_size):
    for x in range(x_size):
        # if bm[x,z]==1:
        #     level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"stone_brick_slab")
        # if qm[x,z]==0:
        #     level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"stone_brick_slab")
        # if qm[x,z]==1:
        #     level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start)-1,z+z_start,"smooth_red_sandstone_slab")
        pass
level.flush()

QL = level.getQuadtreeList()
from Prototypes import Prototypes
from wfc import *
prototypes = Prototypes(level=level)
bd =prototypes.read("prototypes_stone_27.txt")
wfc = WFC(10,15,10,bd,AUTO=0)
bd2 = prototypes.read("prototypes_27.txt")
wfc2 = WFC(10,15,10,bd,AUTO=0)
Area_49 = QL
print(len(Area_49))
Area_49_n = int(len(Area_49) * 0.8)
for p in Area_49[0:Area_49_n]:
    x = x_start + p[0][0]
    z = z_start +p[0][1]
    y = level.getHeightAt(x,z)
    size=(p[1][0],p[1][1])

    mx = x;my=y;mz=z

    for i in range (size[0]):
        for j in range (size[1]):
            if my > level.getHeightAt(x+i,z+j):
                my = level.getHeightAt(x+i,z+j)
    b_base = buildingData(level,"fence_base1.txt")
    b_base.build(x,my,z)
    # my +=1
        
    for i in range (size[0]):
        for j in range (size[1]):
            for k in range(3,10):
                if k==0:
                    # level.setBlock(x+i,my,z+j,"minecraft:polished_andesite")
                    pass
                else:
                    level.setBlock(x+i,my+k,z+j,"air")

    flag = random.choice([0,0])
    if flag == 0:
        if is_sand(level,x,y-1,z):
            r=False
            while r==False:
                r = wfc2.run(level=level,visualize=False)
            print(r)
            
            if(size[0]>=40 and size[1]>=40):
                wfc2.setBuilding(x+2,my+1,z+2)
        else:
            r=False
            while r==False:
                r = wfc.run(level=level,visualize=False)
            print(r)
            
            if(size[0]>=40 and size[1]>=40):
                wfc.setBuilding(x+2,my+1,z+2)
    if flag ==1 :
        if(size[0]>=40 and size[1]>=40):
            c = Cityscape(level, 40, x+3, my+1, z+3, 1, 24, 0, 5, 2, (180, 182, 0, 179, 0))
            c.build()
            c = Cityscape(level, 40, x+18, my+1, z+3, 1, 24, 0, 5, 2, (180, 182, 0, 179, 0))
            c.build()
            c = Cityscape(level, 40, x+33, my+1, z+3, 1, 24, 0, 5, 2, (180, 182, 0, 179, 0))
            c.build()
for p in Area_49[Area_49_n:]:
    x = x_start + p[0][0]
    z = z_start +p[0][1]
    y = level.getHeightAt(x,z)
    size=(p[1][0],p[1][1])
    
    mx = x;my=y;mz=z
    for i in range (size[0]):
        for j in range (size[1]):
            if my > level.getHeightAt(x+i,z+j):
                my = level.getHeightAt(x+i,z+j)
    b_base = buildingData(level,"fence_base1.txt")
    b_base.build(x,my,z)
    # my +=1
    for i in range (size[0]):
        for j in range (size[1]):
            for k in range(2,10):
                if k==0:
                    # level.setBlock(x+i,my,z+j,"minecraft:polished_andesite")
                    pass
                else:
                    level.setBlock(x+i,my+k,z+j,"air")
    if(size[0]>=40 and size[1]>=40):
        if is_sand(level,x,y-1,z):
            c = Cityscape(level, 40, x+3, my+1, z+3, 1, 24, 0, 5, 2, (180, 182, 0, 179, 0))
            c.build()
            c = Cityscape(level, 40, x+18, my+1, z+3, 1, 24, 0, 5, 2, (180, 182, 0, 179, 0))
            c.build()
            c = Cityscape(level, 40, x+33, my+1, z+3, 1, 24, 0, 5, 2, (180, 182, 0, 179, 0))
            c.build()
        else:
            c = Cityscape(level, 40, x+3, my+1, z+3, 1,17,0,5,0,(109, 44, 5, 43, 5))
            c.build()
            c = Cityscape(level, 40, x+18, my+1, z+3, 1,17,0,5,0,(109, 44, 5, 43, 5))
            c.build()
            c = Cityscape(level, 40, x+33, my+1, z+3, 1,17,0,5,0,(109, 44, 5, 43, 5))
            c.build()
# -------------- 20x20
level.calculate_Quadtree(mgw =3,mfw=1,qms = 30,qi=1)
#level.plotMap()
qm = level.getQuadtree()
QL = level.getQuadtreeList()
Area_24 = QL
pc = 0
material_dict={}
material_dict["tree_ID"] = (17, 0)
material_dict["wood_ID"] = (5, 0)
material_dict["fence_id"] = (43, 3, 191)
material_dict["floor_id"] = (1, 6)
roof_ID = (109, 44, 5, 43, 5)
material_dict["roof_ID"] = roof_ID

from building.pagoda import Pagoda_builder
from building.Shrine import Shrine_Builder
for p in QL:
    x = x_start + p[0][0]
    z = z_start +p[0][1]
    y = level.getHeightAt(x,z)
    size=(p[1][0],p[1][1])

    mx = x;my=y;mz=z
    
    for i in range (size[0]):
        for j in range (size[1]):
            if my > level.getHeightAt(x+i,z+j):
                my = level.getHeightAt(x+i,z+j)
    my +=1
    
    level.flush()
    flag = random.choice([0,1])
    if flag==0:
        if pc < 2:
            for i in range (20):
                for j in range (20):
                    for k in range(20):
                        if k==0:
                            level.setBlock(x+i,my,z+j,"minecraft:polished_andesite")
                        else:
                            level.setBlock(x+i,my+k,z+j,"air")
            # b_p =Pagoda_builder(level, x,my,z,
            #                             material_dict["tree_ID"][0],
            #                             material_dict["tree_ID"][1], material_dict["wood_ID"][0],
            #                             material_dict["wood_ID"][1],
            #                             material_dict["roof_ID"])
            if is_sand(level,x,y-1,z):
                b_p =Pagoda_builder(level, x,my,z,24,0,5,2, (180, 182, 0, 179, 0))
            else:
                b_p =Pagoda_builder(level, x,my,z,17,0,5,0,(109, 44, 5, 43, 5))
                b_p.build()
                pc+=1
        else:
            # for i in range ():
            #     for j in range (size[1]):
            #         for k in range(10):
            #             if k==0:
            #                 level.setBlock(x+i,my,z+j,"minecraft:polished_andesite")
            #             else:
            #                 level.setBlock(x+i,my+k,z+j,"air")
            # r=False
            # while r==False:
            #     r = wfc.run(level=level,visualize=False)
            # print(r)
            
            # if(size[0]>=20 and size[1]>=20):
            #     wfc.setBuilding(x,my+1,z)   
            pass
    if flag==1:
        for i in range (20):
            for j in range (20):
                for k in range(20):
                    if k==0:
                        level.setBlock(x+i,my,z+j,"minecraft:polished_andesite")
                    else:
                        level.setBlock(x+i,my+k,z+j,"air")
        b_s =Shrine_Builder(level,x,my+1,z,0,
                                material_dict["tree_ID"][0],
                                material_dict["tree_ID"][1], material_dict["wood_ID"][0],
                                material_dict["wood_ID"][1],
                                material_dict["roof_ID"])
        b_s.build()
# -------------------- 12x12

level.calculate_Quadtree(mgw =1,mfw=1,qms = 10,qi=1)
qm = level.getQuadtree()
#level.plotMap()

for z in range(z_size):
    for x in range(x_size):
        # if bm[x,z]==1:
        #     level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"stone_brick_slab")
        # if qm[x,z]==0:
        #     level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"stone_brick_slab")
        # if qm[x,z]==1:
        #     level.setBlock(x+x_start,level.getHeightAt(x+x_start,z+z_start),z+z_start,"smooth_red_sandstone_slab")
        pass

level.flush()

QL = level.getQuadtreeList()
Area_12 = QL
print(QL)
print(Area_49)
wfc_area_12,house_area_10 =include_list(Area_12,Area_49)
print(wfc_area_12)
b_wfc_12 = buildingData(level,"garden.txt")
for p in wfc_area_12:
    x = x_start + p[0][0]
    z = z_start +p[0][1]
    y = level.getHeightAt(x,z)
    b_wfc_12.build(x,y-1,z)

b_10x10 = buildingData(level,"house_post_12.txt")
b_sand_10x10 =buildingData(level,"house_10x10.txt")
for p in house_area_10:
    x = x_start + p[0][0]
    z = z_start +p[0][1]
    y = level.getHeightAt(x,z)
    if is_sand(level,x,y-1,z):
        b_sand_10x10.build(x,y,z)
    else:
        b_10x10.build(x,y,z)
# b_10x10 = buildingData(level,"house_10x10.txt")
# b_5x5 = buildingData(level,"house_5x5.txt")
# b_7x7 = buildingData(level,"7x7cube.txt")
# # b.build(x_center,level.getHeightAt(x_center,z_center),z_center)
# for p in QL:
#     x = x_start + p[0][0]
#     z = z_start +p[0][1]
#     y = level.getHeightAt(x,z)
#     size=(p[1][0],p[1][1])
#     if(size[0]==7 and size[1]==7):
#         b_7x7.build(x,y,z)
#     elif (size[0] <7 or size[1] <7) and size[0] > 5 and size[1]>5:
#         b_5x5.build(x,y,z)
    
#     elif p[1][0] >10 and p[1][1] >10:
#         b_10x10.build(x,y,z)
# level.flush()

# if QL ==[]:
#     flag=1
#     level.calculate_Quadtree(mgw =1,mfw=1,qms = 8,qi=1)
#     QL = level.getQuadtreeList()
#     for p in QL:
#         if flag:
#             x = x_start + p[0][0]
#             z = z_start +p[0][1]
#             y = level.getHeightAt(x,z)
#             size=(p[1][0],p[1][1])
#             b_5x5 = buildingData(level,"house_5x5_wood.txt")
#             b_5x5.build(x,y,z)
#             flag=0
#         else:
#             flag=1
# import time

# time.sleep(30)
# print("undo")
# level.undo()

